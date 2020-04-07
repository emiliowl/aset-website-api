class ModelCore(object):
    def update_values(self, newdata):
        for key,value in newdata.items():
            setattr(self, key, value)
            