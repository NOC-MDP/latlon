/* Python - C interface for accessing latlon <-> UTM conversion functions
   as used in Webb Research's slocum glider
   
   20 July, lmm@noc.soton.ac.uk Initial 
*/
#include "Python.h"
#include "local.h"
#include "latlon.h"

/* Python object function definitions. */

static PyObject *
_latlonUTM_latlon2UTM(PyObject *self, PyObject *args)
{
  double lat;
  double lon;
  double easting;
  double northing;
  double zone_num;
  double zone_char;
  char zone_str[2];
  // we expect two doubles
  if (!PyArg_ParseTuple(args, "dd", &lat,&lon))
        return NULL;

  latlon_to_utm(lat, lon,
		&zone_num, &zone_char,
		&northing, &easting);
  zone_str[0]=(char)((int)zone_char+65);
  zone_str[1]='\0';
  return Py_BuildValue("(dd)is", easting, northing,\
		       (int)zone_num,zone_str);
}


static PyObject *
_latlonUTM_UTM2latlon(PyObject *self, PyObject *args)
{
  double lat;
  double lon;
  double easting;
  double northing;
  int zone_num;
  char *zone_char;

  // we expect an int, string and two doubles
  if (!PyArg_ParseTuple(args, "isdd", \
			&zone_num,&zone_char,&easting,&northing))
        return NULL;
  utm_to_latlon((double) zone_num,(double) zone_char[0]-65,\
		northing,easting,&lat,&lon);
  return Py_BuildValue("(dd)", lat,lon);
}

/* defining python method names to C function definitions. Not that the last entry should be Null,Null, 0, Null.
   This is to tell Python there are no more functions defined.
*/
static PyMethodDef _latlonUTM_methods[]={
  /* {format is python_name,C_name,1,'docstring'} */
  {"latlon2UTM",_latlonUTM_latlon2UTM,1,
   "This method converts a lat/lon pair into UTM easting/northing pair."},
  {"UTM2latlon",_latlonUTM_UTM2latlon,1,
   "This method converts a zone_num,zone_char, easting/northing pair into UTM easting/northing pair."},
  {NULL,NULL,0,NULL}
};




#if PY_MAJOR_VERSION <3
/* Initialise the module. */
PyMODINIT_FUNC
init_latlonUTM(void)
{
  Py_InitModule("_latlonUTM", _latlonUTM_methods);
}
#else
/*python3 module initialisation */
static struct PyModuleDef _latlonUTM_module = {
  PyModuleDef_HEAD_INIT,
  "_latlonUTM", /*name of module */
  "DOCO (Todo)",
  -1,
  _latlonUTM_methods
};

PyMODINIT_FUNC
PyInit__latlonUTM(void){
  PyObject *mod;
  mod = PyModule_Create(&_latlonUTM_module);
  /* not sure what this does:*/
  //PyModule_AddIntMacro(mod,MAGIC);
  return mod;
};
#endif


