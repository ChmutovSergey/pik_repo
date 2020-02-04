import colander


class BuildingValidator(colander.MappingSchema):
    address = colander.SchemaNode(colander.String(), missing=None)
    year = colander.SchemaNode(colander.Integer(), missing=None)


class BuildingsValidator(colander.SequenceSchema):
    building = BuildingValidator()


class BricksValidator(colander.MappingSchema):
    count_bricks = colander.SchemaNode(colander.Integer(), missing=None)


def get_data(data: dict, schema):
    return schema.serialize(data)
