import submitter,Manager
import CrystalWriter,CrystalRunner,CrystalReader
import PropertiesRunner,PropertiesReader
import os,json


setup={'id':'si'}
setup['crystal']=CrystalWriter.CrystalWriter(cif=open("si.cif").read())
setup['crystal'].set_options({
    'xml_name':"../BFD_Library.xml",
    'kmesh':[2,2,2],
    'basis_params':[0.3,1,3],
    'tolinteg':[8,8,8,8,16],
    'spin_polarized':False,
    'dftgrid':'LGRID'
  })

testjob = Manager.CrystalManager(
    writer=setup['crystal'],
    crys_reader=CrystalReader.CrystalReader(),
    crys_runner=CrystalRunner.LocalCrystalRunner(),
    prop_reader=PropertiesReader.PropertiesReader(),
    prop_runner=PropertiesRunner.LocalPropertiesRunner()
  )

currwd=os.getcwd()
d=setup['id']
try:
  os.mkdir(d)
except:
  pass
os.chdir(d)

testjob.update_status()

