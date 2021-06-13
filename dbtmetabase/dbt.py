import logging
import yaml
import re
from pathlib import Path

# Allowed metabase.* fields
_META_FIELDS = [
    "semantic_type",
    "visibility_type",
]


class DbtReader:
    """Reader for dbt project configuration."""

    def __init__(self, project_path: str):
        """Constructor.

        Arguments:
            project_path {str} -- Path to dbt project root.
        """

        self.project_path = project_path

    def read_models(self, includes=None, excludes=None) -> list:
        """Reads dbt models in Metabase-friendly format.

        Keyword Arguments:
            includes {list} -- Model names to limit processing to. (default: {None})
            excludes {list} -- Model names to exclude. (default: {None})

        Returns:
            list -- List of dbt models in Metabase-friendly format.
        """

        if includes is None:
            includes = []
        if excludes is None:
            excludes = []

        mb_models = []

        for path in (Path(self.project_path) / "models").rglob("*.yml"):
            logging.info("Processing model: %s", path)
            with open(path, "r") as stream:
                schema = yaml.safe_load(stream)
                if schema is None:
                    logging.warning("Skipping empty or invalid YAML: %s", path)
                    continue
                for model in schema.get("models", []):
                    name = model.get("identifier", model["name"])
                    logging.info("Model: %s", name)
                    if (not includes or name in includes) and (name not in excludes):
                        mb_models.append(self.read_model(model))
                for source in schema.get("sources", []):
                    for model in source.get("tables", []):
                        name = model.get("identifier", model["name"])
                        logging.info("Source: %s", name)
                        if (not includes or name in includes) and (
                            name not in excludes
                        ):
                            mb_models.append(self.read_model(model))

        return mb_models

    def read_model(self, model: dict) -> dict:
        """Reads one dbt model in Metabase-friendly format.

        Arguments:
            model {dict} -- One dbt model to read.

        Returns:
            dict -- One dbt model in Metabase-friendly format.
        """

        mb_columns = []

        for column in model.get("columns", []):
            mb_columns.append(self.read_column(column))

        return {
            "name": model.get("identifier", model["name"]).upper(),
            "description": model.get("description"),
            "columns": mb_columns,
        }

    def read_column(self, column: dict) -> dict:
        """Reads one dbt column in Metabase-friendly format.

        Arguments:
            column {dict} -- One dbt column to read.

        Returns:
            dict -- One dbt column in Metabase-friendly format.
        """

        mb_column = {
            "name": column.get("name", "").upper(),
            "description": column.get("description"),
        }

        for test in column.get("tests", []):
            if isinstance(test, dict):
                if "relationships" in test:
                    relationships = test["relationships"]
                    mb_column["semantic_type"] = "type/FK"
                    mb_column["fk_target_table"] = (
                        column.get("meta", {})
                        .get("metabase.fk_ref", self.parse_ref(relationships["to"]))
                        .upper()
                    )
                    mb_column["fk_target_field"] = relationships["field"].upper()

        if "meta" in column:
            meta = column.get("meta", {})
            for field in _META_FIELDS:
                if f"metabase.{field}" in meta:
                    mb_column[field] = meta[f"metabase.{field}"]

            # remove deprecation in future
            if "metabase.special_type" in meta:
                logging.warning(
                    "DEPRECATION: metabase.special_type is deprecated and will be removed, use metabase.semantic_type instead"
                )
                if "semantic_type" not in mb_column:
                    mb_column["semantic_type"] = meta["metabase.special_type"]

        return mb_column

    @staticmethod
    def parse_ref(text: str) -> str:
        """Parses dbt ref() statement.

        Arguments:
            text {str} -- Full statement in dbt YAML.

        Returns:
            str -- Name of the reference.
        """

        matches = re.findall(r"ref\(['\"]([\w\_\-\ ]+)['\"]\)", text)
        if matches:
            return matches[0]
        return text
