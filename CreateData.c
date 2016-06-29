/*  Example of wrapping the cos function from math.h using the Numpy-C-API. */

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>

/*  wrapped cosine function */
static PyObject* cos_func_np(PyObject* self, PyObject* args)
{

    int width;
    int height;
    PyArrayObject *in_array_tu;
    PyArrayObject *in_array_tv;
    PyArrayObject *in_array_refdata;
    //PyArrayObject *in_array_savedata;
    //PyObject      *out_array;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!O!",&width,&height, &PyArray_Type, &in_array_tu, &PyArray_Type, &in_array_tv,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      npy_int32 *datatu = (npy_int32*)   PyArray_DATA(in_array_tu);
      npy_int32 *datatv = (npy_int32*)   PyArray_DATA(in_array_tv);
      npy_int32 *dataref = (npy_int32*)   PyArray_DATA(in_array_refdata);
      //datasave = (npy_int32*)   PyArray_DATA(in_array_savedata);

    npy_intp dims[2] = {width,height};
    PyObject *savedata = PyArray_SimpleNew(2, dims, NPY_INT);
    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);
    int i =0;
    int j =0;
    for( i =0 ;i < width;i++)
     {
        for( j = 0;j<height;j++)
        {
            //npy_intp d[2] = {i,j};
           // PyArray_ITER_GOTO(save_iter,d);
           *(save_iter->dataptr) = 999;
           PyArray_ITER_NEXT(save_iter);
            //savedata[i*width+j]->dataptr = 1;
        }
     }

    /*  clean up and return the result */
    Py_DECREF(in_array_tu);
    Py_DECREF(in_array_tv);
    Py_DECREF(in_array_refdata);
    Py_DECREF(save_iter);
    Py_INCREF(savedata);
    return savedata;

    /*  in case bad things happen */
    fail:
        Py_XDECREF(in_array_tu);
        Py_XDECREF(in_array_tv);
        Py_XDECREF(in_array_refdata);
        return NULL;
}

/*  define functions in module */
static PyMethodDef CosMethods[] =
{
     {"cos_func_np", cos_func_np, METH_VARARGS,
         "evaluate the cosine on a numpy array"},
     {NULL, NULL, 0, NULL}
};

/* module initialization */
PyMODINIT_FUNC

initcos_module_np(void)
{
     (void) Py_InitModule("cos_module_np", CosMethods);
     /* IMPORTANT: this must be called */
     import_array();
}