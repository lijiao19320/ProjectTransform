#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>


// Forward function declaration.
static PyObject *CreateData(PyObject *self, PyObject *args);
{
    int width;
    int height;
    PyArrayObject *in_tu;
    PyArrayObject *in_tv;
    PyArrayObject *in_refData;

    PyObject      *out_array;
    PyArrayIterObject *in_iter;
    PyArrayIterObject *out_iter;

    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!O!", &width,&height,&PyArray_Type, &in_tu,&PyArray_Type, &in_tv,&PyArray_Type, &in_refData))
        return NULL;
}

// Boilerplate: method list.
static PyMethodDef methods[] = {
  { "CreateData", CreateData, METH_VARARGS, "Doc string.----------------mj g"},
  { NULL, NULL, 0, NULL } /* Sentinel */
};

// Boilerplate: Module initialization.
PyMODINIT_FUNC initndmqc(void) {
  (void) Py_InitModule("ProjTransform_C", methods);
  import_array();
}
/**