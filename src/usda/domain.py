#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass
import pprint

class UsdaObject(ABC):
    """
    An abstract base class for all USDA result objects.
    """

    @staticmethod
    @abstractmethod
    def from_response_data(response_data):
        """
        Generate an object from JSON response data.
        
        Params:
            response_data (dict): Parsed JSON response data from the API.
        """
        raise NotImplementedError

    def __getitem__(self, name):
        return getattr(self, name)

    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def __str__(self):
        return pprint.pformat(self.__dict__)

class AbridgedFoodNutrient(UsdaObject):
    """
    Class to represent a FDC AbridgedFoodNutrient object

    Params:
        number (int): FDC Nutrient number, example: 303
        name (str): FDC Nutrient name, example: Iron, Fe
        amount (float): Measure of nutrient, example: 0.53
        unit (str): Unit name, example: mg
        der_code (str): FDC Derivation Code, example: LCCD
        der_desc (str): Derivation description, example: Calculated from a daily value percentage per serving size measure
    """

    @staticmethod
    def from_response_data(response_data):
        return AbridgedFoodNutrient(
            number=response_data.get("number", response_data.get('nutrientNumber')),
            name=response_data.get("name", response_data.get('nutrientName')),
            amount=response_data.get("amount"),
            unit=response_data.get("unitName"),
            der_code=response_data.get("derivationCode"),
            der_desc=response_data.get("derivationDescription"))

    def __init__(self, number, name, amount, unit, der_code, der_desc):

        super(AbridgedFoodNutrient, self).__init__()
        self.number=number
        self.name=name
        self.amount=amount
        self.unit=unit
        self.der_code=der_code
        self.der_desc=der_desc

    def __repr(self):
        return "{} Num: {}, Name: {}".format(self.__class__.__name__, self.number, self.name)

    def __str__(self):
        out_str = ""
        for attr in self.__dict__:
            out_str += attr.__str__() + "\n"
        return out_str

class Nutrient(UsdaObject):
    """
    Class representing a FDC Nutrient

    Params:
        n_id (int): FDC Food Nutrient ID, example: 1005
        number (str): FDC Food Nutrient Number, example: 305
        name (str): FDC Nutrient name, example: Iron, Fe
        rank (int): Nutrient rank, example: 1110
        unit (str): Unit name, example: mg
    """

    @staticmethod
    def from_response_data(response_data):
        return Nutrient(
            n_id=response_data.get('id', response_data.get('nutrientId')),
            number=response_data.get("number", response_data.get('nutrientNumber')),
            name=response_data.get("name", response_data.get('nutrientName')),
            rank=response_data.get('rank'),
            unit=response_data.get('unitName'))

    def __init__(self, n_id, number, name, rank, unit):

        super(Nutrient, self).__init__()
        self.nutrient_id = n_id
        self.number=number
        self.name=name
        self.rank=rank
        self.unit=unit

    def __repr__(self):
        return "{} ID: {}, Name: {}".format(self.__class__.__name__, self.nutrient_id, self.name)

    def __str__(self):
        out_str = ""
        for attr in self.__dict__:
            out_str += attr.__str__() + "\n"
        return out_str

class FoodNutrientDerivation(UsdaObject):
    """
    Class representing FDC's FoodNutrientDerivation object

    Params:
        f_id (int): FDC Food Nutrient ID, example: 1005
        code (str): FDC Derivation Code, example: LCCD
        desc (str): Derivation description, example: Calculated from a daily value percentage per serving size measure
        source (FoodNutrientSource): FDC Source for nutrient info
    """

    @staticmethod
    def from_response_data(response_data):
        food_source = response_data.get('foodNutrientSource')
        if food_source:
            food_source = FoodNutrientSource.from_response_data(food_source)
        return FoodNutrientDerivation(
            f_id=response_data['id'],
            code=response_data['code'],
            desc=response_data['description'],
            source=food_source)

    def __init__(self, f_id, code, desc, source=None):

        super(FoodNutrientDerivation, self).__init__()
        self.id = f_id
        self.code = code
        self.desc = desc
        self.source = source

    def __repr__(self):
        return "{} for ID: {}".format(self.__class__.__name__, self.id)

    def __str__(self):
        out_str = ""
        for attr in self.__dict__:
            out_str += attr.__str__() + "\n"
        return out_str

class FoodNutrientSource(UsdaObject):
    """
    Class representing a FDC FoodNutrientSource object

    Params:
        a_id (int): Food nutrient source ID, example: 9
        code (str): Food nutrient source code, example: 12
        desc (str): Food nutrient source desc, example: Manufacturer's analytical; partial documentation
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodNutrientSource(
            a_id=response_data['id'],
            code=response_data['code'],
            desc=response_data['description'])

    def __init__(self, a_id, code, desc):

        super(FoodNutrientSource, self).__init__()
        self.id = a_id
        self.code = code
        self.desc = desc

class NutrientAnalysisDetails(UsdaObject):
    """
    Class representing a FDC NutrientAnalysisDetails object

    Params:
        s_id (int): Sub Sample ID, example: 343866
        amount (float): Nutrient amonut, example: 0E-8
        n_id (int): FDC Nutrient ID, example: 1005
        desc (str): Lab method description, example: 10.2135/cropsci2017.04.0244
        desc_orig (str): Original desc
        lab_tech (str): Lab method technique, example: DOI for Beans
        acq_deets (NutrientAcquisitionDetails): Acquistion deatils obj
    """

    @staticmethod
    def from_response_data(response_data):
        acq_deets = response_data.get('nutrientAcquisitionDetails')
        if acq_deets:
            acq_deets = NutrientAcquisitionDetails.from_response_data(acq_deets)
        return NutrientAnalysisDetails(
            s_id=response_data['subSampleId'],
            amount=response_data['amount'],
            n_id=response_data['nutrientId'],
            desc=response_data['labMethodDescription'],
            desc_orig=response_data['labMethodOriginalDescription'],
            lab_tech=response_data['labMethodTechnique'],
            acq_deets=acq_deets)

    def __init__(self, s_id, amount, n_id, desc, desc_orig, lab_tech, acq_deets=None):

        super(NutrientAnalysisDetails, self).__init__()
        self.sample_id = s_id
        self.amount = amount
        self.nutrient_id = n_id
        self.desc = desc
        self.desc_orig = desc_orig
        self.technique = lab_tech
        self.acquisition = acq_deets

    def __repr__(self):
        return "{0} for Nutrient ID: {1}".format(self.__class__.__name__, self.nutrient_id)

    def __str__(self):
        out_str = ""
        for attr in self.__dict__:
            out_str += attr.__str__() + "\n"
        return out_str

class NutrientAcquisitionDetails(UsdaObject):
    """
    Class representing a FDC NutrientAcquisitionDetails 

    Params:
        sample_id (int): FDC Sample ID, example: 321632
        purchase_date (str): Date of sameple acquisition, example: 12/2/2005
        city (str): City the sample is stored in, example: 12/2/2005
        state (str): State the sample is strored in, example: AL
    """

    @staticmethod
    def from_response_data(response_data):
        return NutrientAcquisitionDetails(
            sample_id=response_data['sampleUnitId'],
            purchase_date=response_data['purchaseDate'],
            city=response_data['storeCity'],
            state=response_data['storeState'])

    def __init__(self, sample_id, purchase_date, city, state):

        super(NutrientAcquisitionDetails, self).__init__()
        self.sample_id = sample_id
        self.purchase_date = purchase_date
        self.store_city = city
        self.store_state = state

class FoodNutrient(UsdaObject):
    """
    Class representing a FDC FoodNutrient object

    Params:
        fn_id (int): FDC FoodNutrient ID, example: 167514
        amount (float): Nutrient amonut, example: 0E-8
        data_points (int): Number of data points, example: 49
        d_min (float): Minimum data point value, example: 73.73
        d_max (float): Maximum data point value, example: 91.8
        median (float): Median data point value, example: 90.3
        d_type (str): Data type, example: FoodNutrient
        nutrient (Nutrient) Nutrient obj
        nutrient_derv (FoodNutrientDerivation): FoodNutrientDerivation obj
        nutrient_deets (NutrientAnalysisDetails): NutrientAnalysisDetails obj
    """

    @staticmethod
    def from_response_data(response_data):
        nutrient = response_data.get("nutrient")
        if nutrient:
            nutrient = Nutrient.from_response_data(nutrient)
        nutrDerv = response_data.get('foodNutrientDerivation')
        if nutrDerv:
            nutrDerv = FoodNutrientDerivation.from_response_data(nutrDerv)
        nutrDetails = response_data.get('nutrientAnalysisDetails')
        if nutrDetails:
            nutrDetails = NutrientAnalysisDetails.from_response_data(nutrDetails)
        return FoodNutrient(
            fn_id=response_data['id'],
            amount=response_data.get('amount'),
            data_points=response_data.get('dataPoints'),
            d_min=response_data.get('min'),
            d_max=response_data.get('max'),
            median=response_data.get('median'),
            d_type=response_data.get('type'),
            nutrient=nutrient,
            nutrient_derv=nutrDerv,
            nutrient_deets=nutrDetails)

    def __init__(self, fn_id, amount=None, data_points=None, d_min=None, d_max=None,
                 median=None, d_type=None, nutrient=None, nutrient_derv=None, nutrient_deets=None):

        super(FoodNutrient, self).__init__()
        self.id = fn_id
        self.amount = amount
        self.data_points = data_points
        self.min = d_min
        self.max = d_max
        self.median = median
        self.type = d_type
        self.nutrient = nutrient
        self.nutrient_derv = nutrient_derv
        self.nutrient_deets = nutrient_deets

    def __repr__(self):
        return "{} ID: {}".format(self.__class__.__name__, self.id)

    def __str__(self):
        out_str = ""
        for attr in self.__dict__:
            out_str += attr + ": {}\n".format(self[attr])
        return out_str


class FoodItem(UsdaObject):
    """
    Base class for a FDC Food Item

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodItem(
            fdc_id=response_data["fdcId"],
            data_type=response_data["dataType"],
            desc=response_data["description"])

    def __init__(self, fdc_id, data_type, desc):

        super(FoodItem, self).__init__()
        self.fdc_id = fdc_id
        self.data_type = data_type
        self.desc = desc.strip()

    def __str__(self):
        return self.desc

    def __repr__(self):
        return "{0} ID: {1}, '{2}'".format(self.__class__.__name__, self.fdc_id, self.desc)

class AbridgedFoodItem(FoodItem):
    """
    Class representing a FDC AbridgedFoodItem obj

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        nutrients (list): List of AbridgedFoodNutrient's
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        brand (str): Brand owner, example: Kar Nut Products Company; only applies to Branded Foods
        gtinUpc (str): gtinUpc code, example: 077034085228; only applies to Branded Foods
        ndb_id (str): NDB Number, example: 7954; only applies to Foundation and SRLegacy Food
        food_code (str): Food Code, example: 27415110; only applies to Survey Foods
    """

    @staticmethod
    def from_response_data(response_data):
        abg_nutrients = [AbridgedFoodNutrient.from_response_data(nutrient) for nutrient in response_data["foodNutrients"]]
        return AbridgedFoodItem(
            fdc_id=response_data["fdcId"],
            data_type=response_data["dataType"],
            desc=response_data["description"],
            nutrients=abg_nutrients,
            pub_date=response_data.get("publicationDate"),
            brand=response_data.get('brandOwner'),
            gtinUpc=response_data.get('gtinUpc'),
            ndb_id=response_data.get('ndbNumber'),
            food_code=response_data.get('foodCode'))

    def __init__(self, fdc_id, data_type, desc, nutrients=None, pub_date=None, 
                 brand=None, gtinUpc=None, ndb_id=None, food_code=None):

        super(AbridgedFoodItem, self).__init__(fdc_id, data_type, desc)
        self.nutrients = nutrients if nutrients else "No Nutrient Data for Item"
        self.pub_date = pub_date if pub_date else "No Publication Data for Item"
        self.brand = brand if self.data_type == "Branded" else None
        self.gtinUpc = gtinUpc if self.data_type == "Branded" else  None
        self.ndb_id = ndb_id if self.data_type in ["Foundation", "SR Legacy"] else None
        self.food_code = food_code if self.data_type == "Survey" else None

    def __str__(self):
        if self.brand:
            return "{}: {}".format(self.brand, self.desc)
        return super().__str__()

    def __repr__(self):
        if self.brand:
            return "{0} ID: {1}, '{2}: {3}'".format(self.__class__.__name__, self.fdc_id, self.brand, self.desc)
        return super().__repr__()

class SearchResultFoodItem(AbridgedFoodItem):
    """
    Class representing a SearchResultFood Item obj

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        nutrients (list): List of AbridgedFoodNutrient's
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        brand (str): Brand owner, example: Kar Nut Products Company; only applies to Branded Foods
        gtinUpc (str): gtinUpc code, example: 077034085228; only applies to Branded Foods
        ndb_id (str): NDB Number, example: 7954; only applies to Foundation and SRLegacy Food
        food_code (str): Food Code, example: 27415110; only applies to Survey Foods
        sci_name (str): Scientific name of the food
        extra_desc (str): Any additional description info
        highlight (str): Highlighted fields
        score (float): Relative score indicating how well the food matches the search criteria.
    """

    @staticmethod
    def from_response_data(response_data):
        abg_nutrients = [AbridgedFoodNutrient.from_response_data(nutrient) for nutrient in response_data["foodNutrients"]]
        return SearchResultFoodItem(
            fdc_id=response_data["fdcId"],
            data_type=response_data["dataType"],
            desc=response_data["description"],
            nutrients=abg_nutrients,
            pub_date=response_data.get("publicationDate"),
            brand=response_data.get('brandOwner'),
            gtinUpc=response_data.get('gtinUpc'),
            ndb_id=response_data.get('ndbNumber'),
            food_code=response_data.get('foodCode'),
            sci_name=response_data.get('scientificName'),
            extra_desc=response_data.get('additionalDescriptions'),
            highlight=response_data.get('allHighlightFields'),
            score=response_data.get('score'))


    def __init__(self, fdc_id, data_type, desc, nutrients=None, pub_date=None, 
                 brand=None, gtinUpc=None, ndb_id=None, food_code=None, sci_name=None,
                 extra_desc=None, highlight=None, score=None):

        super(SearchResultFoodItem, self).__init__(fdc_id, data_type, desc, nutrients, pub_date, brand,
                                                   gtinUpc, ndb_id, food_code)
        self.scientific_name = sci_name
        self.extra_desc = extra_desc
        self.highlight_fields = highlight
        self.score = score

class BrandedFoodItem(FoodItem):
    """
    Class representing a SearchResultFood Item obj

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        nutrients (list): List of AbridgedFoodNutrient's
        brand (str): Brand owner, example: Kar Nut Products Company; only applies to Branded Foods
        gtinUpc (str): gtinUpc code, example: 077034085228; only applies to Branded Foods
        food_log (FoodUpdateLog): Log of all updates to the food item in FDC
        labeled_nutr (LabeledNutrients): Mapping of nutrients to their respective values for a Food Item
        source (str): FDC Data source
        food_class (str): FDC Food classification
        house_serving (str): Household serving size
        ing (str): Description of ingedients of Food Item
        mod_date (str): Most recent modification date of food item
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        serving_size (int): Serving size of Food
        serving_unit (str): Serving size unit 
        category (str): Branded food category, example: Popcorn, Peanuts, Seeds & Related Snacks
        avail_date (str): Date the food was first made available publicly
    """

    @staticmethod
    def from_response_data(response_data):
        food_nutrients = [FoodNutrient.from_response_data(nutrient) for nutrient in response_data['foodNutrients']]
        food_log = [FoodUpdateLog.from_response_data(log) for log in response_data.get('foodUpdateLog', [])]
        label_nutrients = LabeledNutrients.from_response_data(response_data.get('labelNutrients', {}))
        return BrandedFoodItem(
            fdc_id=response_data["fdcId"],
            data_type=response_data["dataType"],
            desc=response_data["description"],
            nutrients=food_nutrients,
            brand=response_data['brandOwner'],
            gtinUpc=response_data['gtinUpc'],
            food_log=food_log,
            labeled_nutr=label_nutrients,
            source=response_data.get('dataSource'),
            food_class=response_data.get('foodClass'),
            house_serving=response_data.get('householdServingFullText'),
            ing=response_data.get('ingredients'),
            mod_date=response_data.get('modifiedDate'),
            pub_date=response_data.get('publicationDate'),
            serving_size=response_data.get('servingSize'),
            serving_unit=response_data.get('servingSizeUnit'),
            category=response_data.get('brandedFoodCategory'),
            avail_date=response_data.get('availableDate'))

    def __init__(self, fdc_id, data_type, desc, nutrients, brand, gtinUpc, food_log, labeled_nutr,
                 source=None, food_class=None, house_serving=None, ing=None, mod_date=None, pub_date=None,
                 serving_size=None, serving_unit=None, category=None, avail_date=None):

        super(BrandedFoodItem, self).__init__(fdc_id, data_type, desc)
        self.nutrients = nutrients
        self.brand = brand
        self.gtinUpc = gtinUpc
        self.food_log = food_log
        self.labeled_nutrients = labeled_nutr
        self.data_source = source if source else "No data source available"
        self.food_class = food_class if food_class else "Food class is undefined"
        self.house_serving = house_serving if house_serving else "House serving text is undefined"
        self.ingredients = ing if ing else "No ingredients available"
        self.mod_date = mod_date
        self.pub_date = pub_date
        self.serving_size = serving_size if serving_size else "No Serving Size defined"
        self.serving_unit = serving_unit if serving_size and serving_unit else None
        self.category = category if category else "No category defined"
        self.avail_date = avail_date

    def __str__(self):
        if self.brand:
            return "{}: {}".format(self.brand, self.desc)
        return super().__str__()

    def __repr__(self):
        if self.brand:
            return "{0} ID: {1}, '{2}: {3}'".format(self.__class__.__name__, self.fdc_id, self.brand, self.desc)
        return super().__repr__()


class FoundationFoodItem(FoodItem):
    """
    Class representing a FDC FoundationFoodItem

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        food_class (str): FDC Food classification, example: FinalFood
        foot_note (str): Item footnore
        his_ref (str): Boolean if item is historical reference
        ndb_id (str): FDC NDB Number, example: 9316
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        sci_name (str): Scientific name of the food, example: Fragaria X ananassa
        category (FoodCategory): info about category of the food item
        components (list): List of FoodComponents
        nutrients (list): List of AbridgedFoodNutrients
        portions (list): List of FoodPortion objects
        input_foods (list): List of InputFoodFoundation objects to describe food
        conv_fcts (list): List of NutrientConversionFactors for the different nutrients, example: .ProteinConversionFactor
    """

    @staticmethod
    def from_response_data(response_data):
        category = response_data.get('foodCategory')
        if category:
            category = FoodCategory.from_response_data(category)
        components = response_data.get('foodComponents')
        if components:
            components = [FoodComponent.from_response_data(component) for component in components]
        food_nutrients = [FoodNutrient.from_response_data(nutrient) for nutrient in response_data.get('foodNutrients')]
        portions = response_data.get('foodPortions')
        if portions:
            portions = [FoodPortion.from_response_data(portion) for portion in portions]
        input_foods = response_data.get('inputFoods')
        if input_foods:
            input_foods =[InputFoodFoundation.from_response_data(in_food) for in_food in input_foods]
        conv_fcts = response_data.get('nutrientConversionFactors')
        if conv_fcts:
            conv_fcts = [NutrientConversionFactor.from_response_data(conv_fct) for conv_fct in conv_fcts]
        return FoundationFoodItem(
            fdc_id=response_data['fdc_id'],
            data_type=response_data['dataType'],
            desc=response_data['description'],
            food_class=response_data.get('foodClass'),
            foot_note=response_data.get('footNote'),
            his_ref=response_data.get('isHistoricalReference'),
            ndb_id=response_data.get('ndbNumber'),
            pub_date=response_data.get('publicationDate'),
            sci_name=response_data.get('scientificName'),
            category=category,
            components=components,
            nutrients=food_nutrients,
            portions=portions,
            input_foods=input_foods,
            conv_fcts=conv_fcts)

    def __init__(self, fdc_id, data_type, desc, food_class=None, foot_note=None, his_ref=None,
                 ndb_id=None, pub_date=None, sci_name=None, category=None, components=None,
                 nutrients=None, portions=None, input_foods=None, conv_fcts=None):

        super(FoundationFoodItem, self).__init__(fdc_id, data_type, desc)
        self.nutrients = nutrients
        self.food_class = food_class if food_class else "Food class is undefined"
        self.foot_note = foot_note
        self.is_hist_ref = True if his_ref else False
        self.ndb_id = ndb_id
        self.pub_date = pub_date
        self.scientific_name = sci_name
        self.category = category if category else "No FoodCategory defined"
        self.components = components if components else "No FoodComponents defined"
        self.portions = portions if portions else "No FoodPortions defined"
        self.input_foods = input_foods if input_foods else "No InputFoods defined"
        self.conv_factors = conv_fcts

class SRLegacyFoodItem(FoodItem):
    """
    Class representing a FDC SRLegacyFoodItem

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        food_class (str): FDC Food classification, example: FinalFood
        his_ref (str): Boolean if item is historical reference
        ndb_id (str): FDC NDB Number, example: 9316
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        sci_name (str): Scientific name of the food, example: Fragaria X ananassa
        category (FoodCategory): info about category of the food item
        nutrients (list): List of AbridgedFoodNutrients
        conv_fcts (list): List of NutrientConversionFactors for the different nutrients, example: .ProteinConversionFactor
    """

    @staticmethod
    def from_response_data(response_data):
        category = response_data.get('foodCategory')
        if category:
            category = FoodCategory.from_response_data(category)
        food_nutrients = [FoodNutrient.from_response_data(nutrient) for nutrient in response_data.get('foodNutrients')]
        conv_fcts = response_data.get('nutrientConversionFactors')
        if conv_fcts:
            conv_fcts = [NutrientConversionFactor.from_response_data(conv_fct) for conv_fct in conv_fcts]
        return SRLegacyFoodItem(
            fdc_id=response_data['fdc_id'],
            data_type=response_data['dataType'],
            desc=response_data['description'],
            food_class=response_data.get('foodClass'),
            his_ref=response_data.get('isHistoricalReference'),
            ndb_id=response_data.get('ndbNumber'),
            pub_date=response_data.get('publicationDate'),
            sci_name=response_data.get('scientificName'),
            category=category,
            nutrients=food_nutrients,
            conv_fcts=conv_fcts)

    def __init__(self, fdc_id, data_type, desc, food_class=None, his_ref=None, ndb_id=None,
                 pub_date=None, sci_name=None, category=None, nutrients=None, conv_fcts=None):

        super(SRLegacyFoodItem, self).__init__(fdc_id, data_type, desc)
        self.nutrients = nutrients
        self.food_class = food_class if food_class else "Food class is undefined"
        self.is_hist_ref = True if his_ref else False
        self.ndb_id = ndb_id
        self.pub_date = pub_date
        self.scientific_name = sci_name
        self.category = category if category else "No FoodCategory defined"
        self.conv_factors = conv_fcts

class SurveyFoodItem(FoodItem):
    """
    Class representing a FDC SurveyFoodItem
    
    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        end_date (str): End date for the Food Survey
        food_class (str): FDC Food classification, example: FinalFood
        food_code (str): Food code
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        start_date (str): Start date of Food Survey
        food_attrs (list): List of Food attributes
        portions (list): List of FoodPortion objects
        input_foods (list): List of InputFoodSurvey objects to describe food
        wweia_category (WWeiaFoodCategory): WweiaFoodCategory object
    """

    @staticmethod
    def from_response_data(response_data):
        food_attrs = response_data.get('foodAttributes')
        if food_attrs:
            food_attrs = [FoodAttribute.from_response_data(attr) for attr in food_attrs]
        portions = response_data.get('foodPortions')
        if portions:
            portions = [FoodPortion.from_response_data(portion) for portion in portions]
        input_foods = response_data.get('inputFoods')
        if input_foods:
            input_foods =[InputFoodFoundation.from_response_data(in_food) for in_food in input_foods]
        wweia_category = response_data.get('wweiaFoodCategory')
        if wweia_category:
            wweia_category = WWeiaFoodCategory.from_response_data(wweia_category)
        return SurveyFoodItem(
            fdc_id=response_data['fdcId'],
            data_type=response_data['dataType'],
            desc=response_data['description'],
            end_date=response_data.get('endDate'),
            food_class=response_data.get('foodClass'),
            food_code=response_data.get('foodCode'),
            pub_date=response_data.get('publicationDate'),
            start_date=response_data.get('startDate'),
            food_attrs=food_attrs,
            portions=portions,
            input_foods=input_foods,
            wweia_category=wweia_category)

    def __init__(self, fdc_id, data_type, desc, end_date=None, food_class=None, food_code=None,
                 pub_date=None, start_date=None, food_attrs=None, portions=None, input_foods=None,
                 wweia_category=None):

        super(SurveyFoodItem, self).__init__(fdc_id, data_type, desc)
        self.end_date = end_date
        self.food_class = food_class
        self.food_code = food_code
        self.pub_date = pub_date
        self.start_date = start_date
        self.food_attrs = food_attrs
        self.portions = portions
        self.input_foods = input_foods
        self.wweia_category = wweia_category

class SampleFoodItem(FoodItem):
    """
    Class representing a FDC SampleFooditem

    Params:
        fdc_id (int): FDC Food ID, example: 534358
        data_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        food_class (str): FDC Food classification, example: FinalFood
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        food_attrs (list): List of Food attributes
    """

    @staticmethod
    def from_response_data(response_data):
        food_attrs = response_data.get('foodAttributes')
        if food_attrs:
            food_attrs = [FoodCategory.from_response_data(food_cat) for food_cat in food_attrs]
        return SampleFooditem(
            fdc_id=response_data['fdcId'],
            data_type=response_data.get('dataType', 'Sample'),
            desc=response_data['description'],
            food_class=response_data.get('food_class'),
            pub_date=response_data.get('publicationDate'),
            food_attrs=food_attrs)

    def __init__(self, fdc_id, data_type, desc, food_class=None, pub_date=None, food_attrs=None):

        super(SampleFooditem, self).__init__(fdc_id, data_type, desc)

        self.food_class = food_class
        self.pub_date = pub_date
        self.food_attrs = food_attrs

@dataclass(frozen=True)
class SearchResult(UsdaObject):
    """
    Class representing a FDC SearchResult
    
    Params:
        criteria (FoodSearchCriteria): A copy of the criteria that were used in the search.
        total_hits (int): The total number of foods found matching the search criteria.
        curr_page (int): The current page of results being returned.
        total_pages (int): The total number of pages found matching the search criteria.
        foods (list): List of SearchResultFoodItem's
    """

    @staticmethod
    def from_response_data(response_data):
        foods = [SearchResultFoodItem.from_response_data(food) for food in response_data["foods"]]
        search_criteria = FoodSearchCriteria.from_response_data(response_data['foodSearchCriteria'])
        return SearchResult(
            criteria=search_criteria,
            total_hits=response_data['totalHits'],
            curr_page=response_data['currentPage'],
            total_pages=response_data['totalPages'],
            foods=foods)

    def __init__(self, criteria, total_hits, curr_page, total_pages, foods):

        super(SearchResult, self).__init__()
        object.__setattr__(self, "criteria", criteria)
        object.__setattr__(self, "total_hits", total_hits)
        object.__setattr__(self, "curr_page", curr_page)
        object.__setattr__(self, "total_pages", total_pages)
        object.__setattr__(self, "foods", foods)
        # self.criteria = criteria
        # self.total_hits = total_hits
        # self.curr_page = curr_page
        # self.total_pages = total_pages
        # self.foods = foods

    def __str__(self):

        out_str = "Searh Results based on params: '{}'".format(self.criteria)
        return out_str

    def __repr__(self):
        out_str = "Search Results for '{}'\n".format(self.criteria.query)
        for i in range(1, len(self.foods)+1):
            out_str += "{}: {}\n".format(i, self.foods[i-1])
        return out_str


class FoodUpdateLog(UsdaObject):
    """
    Class representing a FDC FoodUpdateLog
    
    Params:
        fdc_id (int): FDC Food ID, example: 534358
        avail_date (str): Date the food was first made available publicly
        brand (str): Brand owner, example: Kar Nut Products Company; only applies to Branded Foods
        source (str): FDC Data source
        d_type (str): Type of Food Item, example: Branded
        desc (str): Food description, example: NUT 'N BERRY MIX
        food_class (str): FDC Food classification
        gtinUpc (str): gtinUpc code, example: 077034085228; only applies to Branded Foods
        house_serving (str): Household serving size
        ing (str): Description of ingedients of Food Item
        mod_date (str): Most recent modification date of food item
        pub_date (str): Publication date for Food item to FDC, example: 4/1/2019
        serving_size (int): Serving size of Food
        serving_unit (str): Serving size unit 
        category (str): Branded food category, example: Popcorn, Peanuts, Seeds & Related Snacks
        changes (str): Changlog
        food_attrs (list): List of Food attributes
    """

    @staticmethod
    def from_response_data(response_data):
        food_attrs = response_data.get('foodAttributes')
        if food_attrs:
            food_attrs = [FoodAttribute.from_response_data(attr) for attr in food_attrs]
        return FoodUpdateLog(
            fdc_id=response_data.get('fdcId'),
            avail_date=response_data.get('availableDate'),
            brand=response_data.get('brandOwner'),
            source=response_data.get('dataSource'),
            d_type=response_data.get('dataType'),
            desc=response_data.get('description'),
            food_class=response_data.get('foodClass'),
            gtinUpc=response_data.get('gtinUpc'),
            house_serving=response_data.get('householdServingFullText'),
            ing=response_data.get('ingredients'),
            mod_date=response_data.get('modifiedDate'),
            pub_date=response_data.get('publicationDate'),
            serving_size=response_data.get('servingSize'),
            serving_unit=response_data.get('servingSizeUnit'),
            category=response_data.get('brandedFoodCategory'),
            changes=response_data.get('changes'),
            food_attrs=food_attrs)

    def __init__(self, fdc_id=None, avail_date=None, brand=None, source=None, d_type=None,
                 desc=None, food_class=None, gtinUpc=None, house_serving=None, ing=None,
                 mod_date=None, pub_date=None, serving_size=None, serving_unit=None,
                 category=None, changes=None, food_attrs=None):

        super(FoodUpdateLog, self).__init__()
        self.fdc_id = fdc_id
        self.avail_date = avail_date
        self.brand = brand
        self.source = source
        self.data_type = d_type
        self.desc = desc
        self.food_class = food_class
        self.gtinUpc = gtinUpc
        self.house_serving = house_serving
        self.ingredients = ing
        self.mod_date = mod_date
        self.pub_date = pub_date
        self.serving_size = serving_size
        self.serving_unit = serving_unit
        self.category = category
        self.changes = changes
        self.food_attrs = food_attrs

class FoodAttribute(UsdaObject):
    """
    Class representing a FDC FoodAttribute
    
    Params:
        f_id (int): Food Attribute ID
        seq (int): Sequence number, example: 1
        value (str): Attribute info, example: Moisture change: -5.0%
        attr_type (dict): Food Attribute type dict
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodAttribute(
            f_id=response_data.get('id'),
            seq=response_data.get('sequenceNumber'),
            value=response_data.get('value'),
            attr_type=response_data.get('FoodAttributeType'))

    def __init__(self, f_id=None, seq=None, value=None, attr_type=None):

        super(FoodAttribute, self).__init__()
        self.id = f_id
        self.seqNum = seq
        self.value = value
        self.attr_type = attr_type

class FoodCategory(UsdaObject):
    """
    Class representing a FDC FoodCategory

    Params:
        f_id (int): Food Category ID
        code (str): Food category code number, example: 1100
        desc (str): Category description, example: Vegetables and Vegetable Products
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodCategory(
            f_id=response_data.get('id'),
            code=response_data.get('code'),
            desc=response_data.get('description'))

    def __init__(self, f_id=None, code=None, desc=None):

        super(FoodCategory, self).__init__()
        self.id = f_id
        self.code = code
        self.desc = desc
        
class FoodComponent(UsdaObject):
    """
    Class representing a FDC FoodComponent

    Params:
        f_id (int): FoodComponent ID
        name (str): Name of component
        data_points (int): Number of available data points
        gram_weight (float): Weight in grams of component
        is_refuse (bool): isRefuse
        min_year_acq (int): Minimum year Component was acquired, example 2011
        percent_weight (float): Percent weight 
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodComponent(
            f_id=response_data.get('id'),
            name=response_data.get('name'),
            data_points=response_data.get('dataPoints'),
            gram_weight=response_data.get('gramWeight'),
            is_refuse=response_data.get('isRefuse'),
            min_year_acq=response_data.get('minYearAcquired'),
            percent_weight=response_data.get('percentWeight'))

    def __init__(self, f_id=None, name=None, data_points=None, gram_weight=None,
                 is_refuse=None, min_year_acq=None, percent_weight=None):

        super(FoodComponent, self).__init__()
        self.id = f_id
        self.name = name
        self.data_points = data_points
        self.gram_weight = gram_weight
        self.is_refuse = is_refuse
        self.min_year_acq = min_year_acq
        self.percent_weight = percent_weight

class FoodPortion(UsdaObject):
    """
    Class representing a FDC FoodPortion

    Params:
        f_id (int): FoodPortion ID
        amount (float): Amount
        data_points (int): Number of available data points
        gram_weight (float): Weight in grams of component
        min_year_acq (int): Minimum year Component was acquired, example 2011
        modifier (str): Modifier
        desc (str): Portion description, example 1 cup
        seq (int): Sequence number, example 1
        measure_unit (MeasureUnit): MeasureUnit object
    """

    @staticmethod
    def from_response_data(response_data):
        measure_unit = response_data.get('measureUnit')
        if measure_unit:
            measure_unit = MeasureUnit.from_response_data(measure_unit)
        return FoodPortion(
            f_id=response_data.get('id'),
            amount=response_data.get('amount'),
            data_points=response_data.get('dataPoints'),
            gram_weight=response_data.get('gramWeight'),
            min_year_acq=response_data.get('minYearAcquired'),
            modifier=response_data.get('modifier'),
            desc=response_data.get('portionDescription'),
            seq=response_data.get('sequenceNumber'),
            measure_unit=measure_unit)

    def __init__(self, f_id, amount, data_points, gram_weight,
                 min_year_acq, modifier, desc, seq, measure_unit):

        super(FoodPortion, self).__init__()
        self.id = f_id
        self.amount = amount
        self.data_points = data_points
        self.gram_weight = gram_weight
        self.min_year_acq = min_year_acq
        self.modifier = modifier
        self.desc = desc
        self.seqNum = seq
        self.measure_unit = measure_unit
        
class InputFoodFoundation(UsdaObject):
    """
    Class representin a FDC InputFoodFoundation
    Applies to Foundation foods. Not all inputFoods will have all fields.
    
    Params:
        f_id (int): InputFood ID, example: 45551
        desc (str): Description of Food, example: Beef, Tenderloin Roast, select, roasted, comp5, lean (34BLTR)
        input_food (SampleFoodItem): Sample Input food object
    """

    @staticmethod
    def from_response_data(response_data):
        input_food = response_data.get('inputFood')
        if input_food:
            input_food = SampleFoodItem.from_response_data(input_food)
        return InputFoodFoundation(
            f_id=response_data.get('id'),
            desc=response_data.get('foodDescription'),
            input_food=input_food)
        pass

    def __init__(self, f_id, desc, input_food):

        super(InputFoodFoundation, self).__init__()
        self.id = f_id
        self.desc = desc
        self.input_food = input_food

class InputFoodSurvey(object):
    """
    Class representing a FDC InputFoodSurvey    
    Applies to Survey (FNDDS). Not all inputFoods will have all fields.

    Params:
        f_id (int): Food Survey item ID
        amount (float): Amount
        food_desc (str): Description of Input Food, example: Spices, curry powder
        ing_code (int): Ingredient Code
        ing_desc (str): Description of ingredients
        ing_weight (float): Weight of ingredient
        portion_code (str): Portion code, example: 21000
        portion_desc (str): Portion description, example: 1 tablespoon
        seq (int): Sequence number
        survey_flag (int): Flag if object is Survey item or not
        unit (str): Unit of measurement, example: TB
        input_food (SurveyFoodItem): SurveyFoodItem object
        retention_factor (RetentionFactor): RetentionFactor info object
    """

    @staticmethod
    def from_response_data(response_data):
        input_food = response_data.get('inputFood')
        if input_food:
            input_food = SurveyFoodItem.from_response_data(input_food)
        ret_factor = response_data.get('retentionFactor')
        if ret_factor:
            ret_factor = RetentionFactor.from_response_data(ret_factor)
        return InputFoodSurvey(
            f_id=response_data.get('id'),
            amount=response_data.get('amount'),
            food_desc=response_data.get('foodDescription'),
            ing_code=response_data.get('ingredientCode'),
            ing_desc=response_data.get('ingredientDescription'),
            ing_weight=response_data.get('ingredientWeight'),
            portion_code=response_data.get('portionCode'),
            portion_desc=response_data.get('portionDescription'),
            seq=response_data.get('sequenceNumber'),
            survey_flag=response_data.get('surveyFlag'),
            unit=response_data.get('unit'),
            input_food=input_food,
            retention_factor=ret_factor)

    def __init__(self, f_id, amount, food_desc, ing_code, ing_desc, ing_weight, portion_code,
                 portion_desc, seq, survey_flag, unit, input_food, retention_factor):

        super(InputFoodSurvey, self).__init__()
        self.id = f_id
        self.amount = amount
        self.food_desc = food_desc
        self.ing_code = ing_code
        self.ing_desc = ing_desc
        self.ing_weight = ing_weight
        self.portion_code = portion_code
        self.portion_desc = portion_desc
        self.seqNum = seq
        self.survey_flag = survey_flag
        self.unit = unit
        self.input_food = input_food
        self.retention_factor = retention_factor

class MeasureUnit(UsdaObject):
    """
    Class representing a MeasureUnit

    Params:
        m_id (int): Measure Unit ID, example: 999
        abbv (str): Abbreviation of measure name
        name (str): Measure name
    """

    @staticmethod
    def from_response_data(response_data):
        return MeasureUnit(
            m_id=response_data.get('id'),
            abbv=response_data.get('abbreviation'),
            name=response_data.get('name'))

    def __init__(self, m_id, abbv, name):

        super(MeasureUnit, self).__init__()
        self.id = m_id
        self.abbv = abbv
        self.name = name
        
class RetentionFactor(UsdaObject):
    """
    Class representing a FDC RetentionFactor

    Params:
        r_id (int): RetentionFactor ID, example: 235
        code (int): RetentionFactor code, example: 3460
        desc (str): RetentionFactor description, example: VEG, ROOTS, ETC, SAUTEED
    """

    @staticmethod
    def from_response_data(response_data):
        return RetentionFactor(
            r_id=response_data.get('id'),
            code=response_data.get('code'),
            desc=response_data.get('description'))

    def __init__(self, r_id, code, desc):

        super(RetentionFactor, self).__init__()
        self.id = r_id
        self.code = code
        self.desc = desc

class WWeiaFoodCategory(UsdaObject):
    """
    Class representing a FDC WWeiaFoodCategory object
    
    Params:
        code (int): Category code, example: 3002
        desc (str): Category description, example: Meat mixed dishes
    """

    @staticmethod
    def from_response_data(response_data):
        return WWeiaFoodCategory(
            code=response_data.get('wweiaFoodCategoryCode'),
            desc=response_data.get('wweiaFoodCategoryDescription'))

    def __init__(self, code, desc):

        super(WWeiaFoodCategory, self).__init__()
        self.code = code
        self.desc = desc

class FoodSearchCriteria(UsdaObject):
    """
    Class representing a FDC FoodSearchCriteria object
    JSON for request body of 'search' POST request

    Params:
        query (str): Search terms to use in the search. The string may also include standard search operators
        data_type (list): Optional. Filter on a specific data type; specify one or more values in an array.
        page_size (int): Optional. Maximum number of results to return for the current page. Default is 50.
        page_num (int): Optional. Page number to retrieve. The offset into the overall result set is expressed as (pageNumber * pageSize)
        sort_by (str): Optional. Specify one of the possible values to sort by that field.
                       **Note, dataType.keyword will be dataType and lowercaseDescription.keyword will be description in future releases.**
        sort_order (str): Optional. The sort direction for the results. Only applicable if sortBy is specified. 'asc' or 'dsc'
        brand (str): Optional. Filter results based on the brand owner of the food. Only applies to Branded Foods.
    """

    @staticmethod
    def from_response_data(response_data):
        return FoodSearchCriteria(
            query=response_data.get('query'),
            data_type=response_data.get('dataType'),
            page_size=response_data.get('pageSize'),
            page_num=response_data.get('pageNumber'),
            sort_by=response_data.get('sortBy'),
            sort_order=response_data.get('sortOrder'),
            brand=response_data.get('brandOwner'))

    def __init__(self, query, data_type, page_size, page_num,
                 sort_by, sort_order, brand):

        super(FoodSearchCriteria, self).__init__()
        self.query = query
        self.data_type = data_type
        self.page_size = page_size
        self.page_num = page_num
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.brand = brand

class LabeledNutrients(UsdaObject):
    """
    Class representing a LabeledNutrients object

    Params:
        fat (float): Amount of fat in Food item
        sat_fat (float): Amount of saturated fat in Food item
        trans_fat (float): Amount of trans fat in Food item
        cholesterol (float): Amount of cholesterol in Food item
        sodium (float): Amount of sodium in Food item
        carbs (float): Amount of carbohydrates in Food item
        fiber (float): Amount of fiber in Food item
        sugars (float): Amount of sugars in Food item
        protein (float): Amount of protein in Food item
        calcium (float): Amount of calcium in Food item
        iron (float): Amount of iron in Food item
        potassium (float): Amount of potassium in Food item
        calories (float): Amount of calories in Food item
    """
    @staticmethod
    def from_response_data(response_data):
        no_data_str = "No '{}' data available"
        return LabeledNutrients(
            fat=response_data.get('fat', no_data_str.format('fat')),
            sat_fat=response_data.get('saturatedFat', no_data_str.format('saturated fat')),
            trans_fat=response_data.get('transFat', no_data_str.format('trans fat')),
            cholesterol=response_data.get('cholesterol', no_data_str.format('cholesterol')),
            sodium=response_data.get('sodium', no_data_str.format('sodium')),
            carbs=response_data.get('carbohydrates', no_data_str.format('carbohydrates')),
            fiber=response_data.get('fiber', no_data_str.format('fiber')),
            sugars=response_data.get('sugars', no_data_str.format('sugars')),
            protein=response_data.get('protein', no_data_str.format('protein')),
            calcium=response_data.get('calcium', no_data_str.format('calcium')),
            iron=response_data.get('iron', no_data_str.format('iron')),
            potassium=response_data.get('potassium', no_data_str.format('potassium')),
            calories=response_data.get('calories', no_data_str.format('calories')))

    def __init__(self, **kwargs):
        super(LabeledNutrients, self).__init__()
        
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])
        
