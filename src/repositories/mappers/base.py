class DataMapper:
    db_model = None    # модель алхимии
    schema = None      # пайдантик-схема

    #превращаем нашу алхимическую модель в схему пайдантика
    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    # превращаем нашу схему пайдантика в алхимическую модель
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
