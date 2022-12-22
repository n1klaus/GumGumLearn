#!/usr/bin/python3
from backend.engine import storage
from backend.models.user import UserOrm
from backend.models.vault import VaultOrm
from backend.models.search import SearchOrm

classes = {
    "User": UserOrm,
    "Vault": VaultOrm,
    "Search": SearchOrm,
}

for cls in classes.values():
    if cls == UserOrm:
        kwargs = {
            "username": "Kizaru",
            "password": "89131231234342"
        }
        my_model = UserOrm(**kwargs)
        user_id = my_model.user_id
    if cls == VaultOrm:
        kwargs = {
            "name": "Akainu",
            "count": "12"
        }
        my_model = VaultOrm(**kwargs)
        my_model.save()
        # vault_id = my_model.vault_id
    elif cls == SearchOrm:
        kwargs = {
            "word": "Nakama"
        }
        my_model = SearchOrm(**kwargs)
        search_id = my_model.search_id

    my_model.save()
    print('\n<---->')
    # my_model = cls[1].from_orm(my_model)
    print(my_model)

    print('\n<---->')
    my_model_json = my_model.to_dict()
    print(my_model_json)

    print('\n<---->')
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key,
                                       type(my_model_json[key]),
                                       my_model_json[key]))

    print('\n<---->')
    print("All objects: {}".format(storage.count()))
    print("{} objects: {}".format(cls.__name__, storage.count(cls)))

    print('\n<---->')
    first_cls_id = list(storage.all(cls).values())[0].id
    print("First {}: {}".format(str(cls.__name__).lower(),
                                str(storage.get(cls, first_cls_id))))

    # print('\n<---->')
    # my_model.delete()
    # print(storage.all().get(
    #     f"{my_model.__class__.__name__}.{my_model.id}"))
