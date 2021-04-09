# python-usda-fdc

python-usda-fdc provides an interface for interacting with [USDA's Food Data Central API ](https://fdc.nal.usda.gov/api-guide.html).

## Installation

```
pip install python-usda-fdc
```

## Usage

``` python
from usda.client import UsdaClient

client = UsdaClient("YOUR_API_KEY")
foods = client.list_foods(page_size=5)

for food in foods:
    print(food)
```

Result:

```
Abiyuch, raw
Acerola juice, raw
Acerola, (west indian cherry), raw
Acorn stew (Apache)
Agave, cooked (Southwest)
```