import urllib2;
from lxml import etree;
from bs4 import BeautifulSoup;
from Writer import Writer;
from sets import Set;


########################################################################
class Parser:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.base = "http://www.icd10data.com";
        self.writer = Writer("temp.txt");
        self.direction = Set(["right","left"]);
        self.areas = [u'finger(s)', u'leg',u'thigh', u'femur', u'thumb', u'jaw', u'pelvic region and thigh', 
                      u'initial encounter for fracture', u'humerus', 'joint', u'foot', u'mid-cervical region', 
                      u"angle's class ii", 'shoulder', u'ankle and toes', u'occipito-atlanto-axial region', u'bone',
                      u'ulna and radius', u'ring finger',  u'thoracolumbar region', u'tibia and fibula', u'vertebrae', 
                      u'ankle and joints of foot', u'arm', u'thoracic region', u'lumbar region', u'distal tibia', 
                      u'finger', u'ulna', u'subsequent encounter for fracture with malunion', 'head region', 
                      u'little finger', u"angle's class iii", u'with tophus (tophi)', u'fibula', u'central', 
                      u'proximal tibia', u'radius and ulna',u'radius', u'upper arm', u'organ involvement unspecified', 
                      u'bone plate', u'upper arms', u'high cervical region', u'excluding foot', 
                      u'distal femur', u'middle finger', u'distal humerus', u'subsequent encounter for fracture with nonunion', 
                      u'ankle', u'joints of hand', u'multiple sites in spine', u'sequela', u'proximal femur', u'index finger', 
                      u'distal radius', u'ear', u'organ or system involvement unspecified', u'sequela of fracture', 
                      u'without tophus (tophi)', u'with other organ involvement', u'with respiratory involvement', 'elbow', 
                      u'lumbosacral region', u'hip', u'forearm', u'thoracolumbar and lumbosacral intervertebral disc disorder', 
                      u'pelvis', u'toe(s)', u'proximal humerus', u'tibia', u'with myopathy', 
                      u'subsequent encounter for fracture with routine healing', u'ankle and joints of foot', u'hand', u'finger joints', 
                      u'wrist', u'overuse and pressure other site', u'ankle and foot', u'knee', u'cervicothoracic region', 
                      u"angle's class i", u'cervical region', 'vertebra', u'upper limb', u'sacral and sacrococcygeal region',  u'lower leg'];
        self.areas.sort(key=lambda x: len(x.split(" ")),reverse=True);
        
    #----------------------------------------------------------------------
    def getmainlist(self):
        """"""
        response = urllib2.urlopen("http://www.icd10data.com/ICD10CM/Codes/M00-M99");
        self.htmlparser = etree.HTMLParser()
        tree = etree.parse(response, self.htmlparser);  
        self.hreflist = tree.xpath("/html/body/div[2]/div/div[4]/ul/li/a/@href");
        self.hreflist = self.hreflist;
        self.getsublist(self.hreflist);
        self.writer.close();
    
    #----------------------------------------------------------------------
    def getsublist(self,hreflist):
        """"""
        for href in hreflist:
            response = urllib2.urlopen(self.base+href);
            soup = BeautifulSoup(response.read(),"lxml");
            lists = soup.select("ul li span a");
            for l in lists:
                self.selectcode(l.attrs["href"]);
            
    #----------------------------------------------------------------------
    def selectcode(self,link):
        """"""
        response = urllib2.urlopen(self.base+link);
        soup = BeautifulSoup(response.read().decode("gbk").encode("utf-8"),"html.parser");
        greenimgs = soup.select('img[src="/images/bullet_triangle_green.png"]');
        for greenimg in greenimgs:
            sibilings = greenimg.parent.findChildren("span");
            code = sibilings[0].a.text;
            description = sibilings[1].text;
            side = "NULL";
            area = "NULL";
            area,side = self.setarea_side(description);
            description = self.setdescription(sibilings[1],sibilings[0].a);
            self.writer.insert(code, description, 10, side, area, 0);

    #----------------------------------------------------------------------
    def setdescription(self,description_obj,link_obj):
        """"""
        if (description_obj.text.find(u"\u2026\u2026")!=-1):
            response = urllib2.urlopen(self.base+link_obj.attrs["href"]);
            soup = BeautifulSoup(response.read().decode("gbk").encode("utf-8"),"html.parser");
            description = soup.select("div div div h2")[0].text;
            return description;
        return description_obj.text;
    
    #----------------------------------------------------------------------
    def setarea_side(self,description):
        """"""
        area = "NULL";
        side = "NULL";
        desc= description;
        for direction in self.direction:
            if (desc.find(direction)!=-1):
                side = direction;
                desc = desc.replace(direction+" ","");
                break;
        for pos in self.areas:
            if (desc.find(pos)!=-1):
                area = pos;
                break;
        if (area=="joint" and side=="NULL"):
            area = "NULL"
        return area, side;

    
if __name__=="__main__":
    parser = Parser();
    #print parser.setarea_side("Staphylococcal arthritis, left shoulder");
    #print parser.setarea_side("Osteochondritis dissecans, joints of left hand");
    #print parser.setarea_side("Direct infection of right shoulder in infectious and parasitic diseases classified elsewhere");
    #print parser.setarea_side("Fracture of tibia or fibula following insertion of orthopedic implant, joint prosthesis, or bone plate, unspecified leg");

    parser.getmainlist();
    
    