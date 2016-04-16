########################################################################
class Writer:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, output):
        """Constructor"""
        self.output = output;
        self.f = open(self.output,"w");
        self.template = "".join(("INSERT INTO `ICDDiagnosticCodes` (`Code`, `Description`, `Version`, `Side`, `Area`, `InferAnatomy`)",
             "VALUES ('%(code)s', '%(description)s', '%(version)s', %(side)s, %(area)s, %(inferanatomy)s;"));
        
        
    #----------------------------------------------------------------------
    def insert(self,code,description,version,side,area,inferanatomy):
        """sample: ('M00.011', 'Staphylococcal arthritis, right shoulder', '10', 'right', 'shoulder', 0)"""
        if area != "NULL":
            area = "'"+area +"'";
        if side!="NULL":
            side = "'"+side+"'";
        self.f.write((self.template % {"code":code,"description":description,
                                      "version":version,"side":side,"area":area,
                                      "inferanatomy":inferanatomy}).encode('utf-8').strip()+"\n");
        
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.f.close();