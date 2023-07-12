from driver.models import Driver
class CabMatchingStratergy:
    @classmethod
    def matchCars(cls,drivers):
        for driver in drivers:
            assert isinstance(driver,Driver)
            if driver.occupiedStatus==False:
                return driver
        return None
