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


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!O!",&width,&height, &PyArray_Type, &in_array_tu, &PyArray_Type, &in_array_tv,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      PyArrayIterObject *tu_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_tu);
      PyArrayIterObject *tv_iter = (PyArrayIterObject* )PyArray_IterNew((PyObject*)in_array_tv);
      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata = PyArray_SimpleNew(2, dims, NPY_INT);

    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int index = 0;
    int count = width*height;

    for(index = 0;index<count;index++)
    {
            int * out_savedataptr = (int *)save_iter->dataptr;
           *(out_savedataptr) = 400;
           PyArray_ITER_NEXT(save_iter);
    }

    int i =0;

    for( i =0 ;i < tu_iter->size;i++)
     {

        {


            int * tudataptr = (int *)tu_iter->dataptr;
            int * tvdataptr = (int *)tv_iter->dataptr;


            int * refdataptr = (int *)ref_iter->dataptr;

            npy_intp savedatadim[2] = {*(tvdataptr),*(tudataptr)};

            PyArray_ITER_GOTO(save_iter,savedatadim);
           int * out_savedataptr = (int *)save_iter->dataptr;
           *(out_savedataptr) = *(refdataptr);

            PyArray_ITER_NEXT(tu_iter);
            PyArray_ITER_NEXT(tv_iter);
            PyArray_ITER_NEXT(ref_iter);

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