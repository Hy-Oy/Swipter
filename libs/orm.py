class ModelToDicMiXin():
    def to_dic(self,exclude=None):
        if exclude == None:
            exclude = []

        attr_dic = {}
        fileds = self._meta.fields

        for filed in fileds:
            filed_name = filed.attname
            if filed_name not in exclude:
                attr_dic[filed_name] = getattr(self, filed_name)

        return attr_dic
