/*  Example of wrapping the cos function from math.h using the Numpy-C-API. */

#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>
#include <stdint.h>

/*  wrapped cosine function */
static PyObject* CreateOutputSearTable(PyObject* self, PyObject* args)
{

    int width;
    int height;
    PyArrayObject *in_array_tu;
    PyArrayObject *in_array_tv;
    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!",&width,&height, &PyArray_Type, &in_array_tu, &PyArray_Type, &in_array_tv))
        return NULL;

      PyArrayIterObject *tu_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_tu);
      PyArrayIterObject *tv_iter = (PyArrayIterObject* )PyArray_IterNew((PyObject*)in_array_tv);
//      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata = PyArray_SimpleNew(2, dims, NPY_INT);

    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int index = 0;
    int count = width*height;

//    for(index = 0;index<count;index++)
//    {
//            int * out_savedataptr = (int *)save_iter->dataptr;
//           *(out_savedataptr) = 400;
//           PyArray_ITER_NEXT(save_iter);
//    }

    int *OD = malloc(sizeof(int)*count);

    for(index = 0;index<count;index++)
    {
            //int * out_savedataptr = (int *)save_iter->dataptr;
           *(OD+index) = 65535;
           //PyArray_ITER_NEXT(save_iter);
    }

    int i =0;

    for( i =0 ;i < tu_iter->size;i++)
     {

        {


            int * tudataptr = (int *)tu_iter->dataptr;
            int * tvdataptr = (int *)tv_iter->dataptr;


//            int * refdataptr = (int *)ref_iter->dataptr;

//            npy_intp savedatadim[2] = {*(tvdataptr),*(tudataptr)};
//
//            PyArray_ITER_GOTO(save_iter,savedatadim);
//           int * out_savedataptr = (int *)save_iter->dataptr;
//           *(out_savedataptr) = *(refdataptr);


//            if((short)(*(refdataptr))<65535)
            {
                int index  =  (*(tvdataptr)) * width+*(tudataptr);
                //*(OD+index) = (int)(*(refdataptr));
                *(OD+index) = i;
            }

            PyArray_ITER_NEXT(tu_iter);
            PyArray_ITER_NEXT(tv_iter);
//            PyArray_ITER_NEXT(ref_iter);

        }
     }

    CFill_Gap_By_NeighbourPoint(OD,width,height,8,65535);


//    CFill_Gap_By_InterpolatingAlongX(OD,width,height, 0 , 65535, 0);

    for(index = 0;index<count;index++)
    {
           int * out_savedataptr = (int *)save_iter->dataptr;
           *(out_savedataptr) = *(OD+index);
           PyArray_ITER_NEXT(save_iter);
    }

    free(OD);
    /*  clean up and return the result */
    Py_DECREF(in_array_tu);
    Py_DECREF(in_array_tv);
//    Py_DECREF(in_array_refdata);
    Py_DECREF(save_iter);
    Py_INCREF(savedata);
    return savedata;

    /*  in case bad things happen */
    fail:
        Py_XDECREF(in_array_tu);
        Py_XDECREF(in_array_tv);
//        Py_XDECREF(in_array_refdata);
        return NULL;
}

/*  wrapped cosine function */
static PyObject* CreateOutputData(PyObject* self, PyObject* args)
{

    int width;
    int height;
    PyArrayObject *in_array_SearchTable;

    PyArrayObject *in_array_refdata;


    /*  parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "iiO!O!",&width,&height, &PyArray_Type, &in_array_SearchTable,
     &PyArray_Type, &in_array_refdata))
        return NULL;

      PyArrayIterObject *Tabel_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_SearchTable);

      PyArrayIterObject *ref_iter = (PyArrayIterObject *)PyArray_IterNew((PyObject*)in_array_refdata);


    npy_intp dims[2] = {height,width};

    PyObject *savedata = PyArray_SimpleNew(2, dims, NPY_INT);

    PyArrayIterObject *save_iter;
    save_iter = (PyArrayIterObject *)PyArray_IterNew(savedata);

    int count = height*width;

    int i =0;

    for( i =0 ;i < count;i++)
     {

        {


            int * tabledataptr = (int *)Tabel_iter->dataptr;
            int * savedataptr = (int *)save_iter->dataptr;




            PyArray_ITER_GOTO1D(ref_iter,*tabledataptr);

            int * refdataptr = (int *)ref_iter->dataptr;
                //int index  =  (*(tvdataptr)) * width+*(tudataptr);
                //*(OD+index) = (int)(*(refdataptr));
             *(savedataptr) = *(refdataptr);

            PyArray_ITER_NEXT(Tabel_iter);
            PyArray_ITER_NEXT(save_iter);


        }
     }

//    printf("testttt");
    /*  clean up and return the result */
    Py_DECREF(in_array_SearchTable);
    Py_DECREF(in_array_refdata);
    Py_DECREF(Tabel_iter);
    Py_DECREF(ref_iter);
    Py_DECREF(save_iter);

    Py_INCREF(savedata);
    return savedata;

    /*  in case bad things happen */
    fail:
        Py_XDECREF(in_array_SearchTable);
        Py_XDECREF(in_array_refdata);
        Py_XDECREF(Tabel_iter);
        return NULL;
}


/*  define functions in module */
static PyMethodDef OutputDataMethods[] =
{
     {"CreateOutputSearTable", CreateOutputSearTable, METH_VARARGS,
         "evaluate the cosine on a numpy array"},
     {"CreateOutputData", CreateOutputData, METH_VARARGS,
         "evaluate the cosine on a numpy array"},
     {NULL, NULL, 0, NULL}
};

/* module initialization */
PyMODINIT_FUNC

initProjOutputData_module(void)
{
     (void) Py_InitModule("ProjOutputData_module", OutputDataMethods);
     /* IMPORTANT: this must be called */
     import_array();
}


void CFill_Gap_By_NeighbourPoint(int *lpDIBorigin, int iImgWidth, int iImgHeight, int iNumberOfRepeat, int iFillValue)
{
    if(lpDIBorigin == NULL)    //DIB has not been allocated
		return;

	int   *pRowUp, *pRowMiddle, *pRowDown, *pRowBuffer,* pRowBuffer0;
	int *lpDataUp, *lpDataDown,*lpDIB;

	//&
	lpDataUp = NULL;

	pRowBuffer0= ( int  * )malloc( iImgWidth * 3 *sizeof(int));
	pRowUp		= pRowBuffer0;
	pRowMiddle  = pRowBuffer0 + iImgWidth;
	pRowDown	= pRowBuffer0 + iImgWidth * 2;

	long i, iRow;
    long myNumberOfRepeat;
	for( myNumberOfRepeat=0; myNumberOfRepeat < iNumberOfRepeat; myNumberOfRepeat++)
	{
		memset( pRowBuffer0, 0, iImgWidth * 3 );

		//for the first line
		lpDIB = lpDIBorigin +1;
		lpDataDown =lpDIB + iImgWidth;

		for( i= 1 ; i < (iImgWidth - 1); i++)
		{
			if (*lpDIB == iFillValue)   //  need to fill a value for this point
			{
				/*					if(m_bIsInOrb[i] == 0){//if(!rgn.PtInRegion (i,iRow)){
				lpDIB ++;
				lpDataUp ++;
				lpDataDown ++;
				continue;
				}
				*/
				if (lpDIB[1] != iFillValue )			// the right point
				{
					*lpDIB =lpDIB[1];		pRowUp[i]=1;
				}
				else if( *lpDataDown != iFillValue )	// the down point
				{
					*lpDIB = *lpDataDown;	pRowUp[i]=1;
				}
				else if (lpDIB[-1] != iFillValue )		// the left point
				{
					*lpDIB =lpDIB[-1];		pRowUp[i]=1;
				}
				else if( lpDataDown[1] != iFillValue )	// the down- right point
				{
					*lpDIB = lpDataDown[1];	pRowUp[i]=1;
				}
				else if (lpDataDown[-1] != iFillValue)	// the down-left point
				{
					*lpDIB =lpDataDown[-1];	pRowUp[i]=1;
				}
			}

			lpDIB ++;
			lpDataUp ++;
			lpDataDown ++;
		}

	//for the internal points
		for (iRow=1; iRow < (iImgHeight-1) ; iRow++)
		{
			lpDIB = lpDIBorigin +  iImgWidth  *  iRow + 1;
			lpDataUp =lpDIB - iImgWidth ;
			lpDataDown =lpDIB + iImgWidth ;

			for( i= 1 ; i < (iImgWidth - 1); i++)
			{
				if (*lpDIB == iFillValue)	//  need to fill a value for this point
				{
					/*if(m_bIsInOrb[iRow*iImgWidth+i] == 0){//if(!rgn.PtInRegion (i,iRow)){
						lpDIB ++;
						lpDataUp ++;
						lpDataDown ++;
						continue;
					}*/
					if (lpDIB[1] != iFillValue && pRowMiddle[i+1] != 1)			// the right point
					{
						*lpDIB =lpDIB[1];			pRowMiddle[i]=1;
					}
					else if( *lpDataDown != iFillValue )						// the down point
					{
						*lpDIB = lpDataDown[0];		pRowMiddle[i]=1;
					}
					else if (lpDIB[-1] != iFillValue && pRowMiddle[i-1] != 1)	// the left point
					{
						*lpDIB =lpDIB[-1];			pRowMiddle[i]=1;
					}
					else if (*lpDataUp != iFillValue && pRowUp[i] != 1)			// the up point
					{
						*lpDIB = lpDataUp[0];		pRowMiddle[i]=1;
					}
					else if ( lpDataUp[1] != iFillValue && pRowUp[i+1] != 1)	// the up- right point
					{
						*lpDIB =  lpDataUp[1];		pRowMiddle[i]=1;
					}
					else if( lpDataDown[1] != iFillValue )						// the down- right point
					{
						*lpDIB = lpDataDown[1];		pRowMiddle[i]=1;
					}
					else if (lpDataDown[-1] != iFillValue)						// the down-left point
					{
						*lpDIB =lpDataDown[-1];		pRowMiddle[i]=1;
					}
					else if (lpDataUp[-1] != iFillValue && pRowUp[i-1] != 1)	// the up-left point
					{
						*lpDIB =lpDataUp[-1];		pRowMiddle[i]=1;
					}
				}

				lpDIB ++;
				lpDataUp ++;
				lpDataDown ++;
			}

			pRowBuffer		= pRowUp;
			pRowUp			= pRowMiddle;
			pRowMiddle		= pRowDown;
			pRowDown		= pRowBuffer;

			memset(pRowDown, 0, iImgWidth);
		}
	}

	// for the last line
	lpDIB		= lpDIBorigin + iImgWidth * (iImgHeight-1) + 1;
	lpDataUp	= lpDIB - iImgWidth;

	for( i= 1 ; i < (iImgWidth- 1 ); i++)
	{
		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[i + iImgWidth  *   (iImgHeight-1)] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	lpDIB ++;
			//	lpDataUp ++;
			//	lpDataDown ++;
			//	continue;
			//}
			//*/
			if (lpDIB[1] != iFillValue && pRowMiddle[i+1] != 1)			// the right point
			{
				*lpDIB =lpDIB[1];
				pRowMiddle[i]=1;
			}
			else if (lpDIB[-1] != iFillValue && pRowMiddle[i-1] != 1)	// the left point
			{
				*lpDIB =lpDIB[-1];
				pRowMiddle[i]=1;
			}
			else if (*lpDataUp != iFillValue && pRowUp[i] != 1)			// the up point
			{
				*lpDIB = lpDataUp[0];
				pRowMiddle[i]=1;
			}
			else if ( lpDataUp[1] != iFillValue && pRowUp[i+1] != 1)	// the up- right point
			{
				*lpDIB =  lpDataUp[1];
				pRowMiddle[i]=1;
			}
			else if (lpDataUp[-1] != iFillValue && pRowUp[i-1] != 1)	// the up-left point
			{
				*lpDIB =lpDataUp[-1];
				pRowMiddle[i]=1;
			}
		}

		lpDIB ++;
		lpDataUp ++;
		lpDataDown ++;
	}

	//for the left column
	lpDIB = lpDIBorigin;

	for(i = 1; i < (iImgHeight - 1); i++)
	{
		lpDIB += iImgWidth;

		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[i * iImgWidth] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	continue;
			//}*/
			if (lpDIB[1] != iFillValue)					// the right point
			{
				*lpDIB = lpDIB[1];
			}
			else if( lpDIB[iImgWidth] != iFillValue)	// the down point
			{
				*lpDIB = lpDIB[iImgWidth];
			}
			else if (lpDIB[-iImgWidth] != iFillValue)	// the up point
			{
				*lpDIB = lpDIB[-iImgWidth];
			}
		}
	}

	//for the right column
	lpDIB = lpDIBorigin + iImgWidth - 1;

	for(i = 1; i < (iImgHeight - 1); i++)
	{
		lpDIB  += iImgWidth;

		if (*lpDIB == iFillValue)	//  need to fill a value for this point
		{
			///*if(m_bIsInOrb[(i+1) * iImgWidth-1] == 0){//if(!rgn.PtInRegion (i,iRow))
			//{
			//	continue;
			//}*/
			if (lpDIB[-1] != iFillValue)				// the left point
			{
				*lpDIB = lpDIB[-1];
			}
			else if( lpDIB[iImgWidth] != iFillValue)	// the down point
			{
				*lpDIB = lpDIB[iImgWidth];
			}
			else if (lpDIB[-iImgWidth] != iFillValue)	// the up point
			{
				*lpDIB = lpDIB[-iImgWidth];
			}
		}
	}

	free(pRowBuffer0);

	return;
}


void CFill_Gap_By_InterpolatingAlongY(unsigned short *lpDIBorigin, int iImgWidth, int iImgHeight, int iInputType, short iFillValue, short iBadData)
{
    if(lpDIBorigin == NULL) return ;   //DIB has not been allocated

	long iCol,  iRow;
	long iYstart,iYend;
	double dV1,dV2;
	short *lpDIB = lpDIBorigin ;
	short *p;
	for( iCol= 0 ; iCol < iImgWidth; iCol++){


		iYstart=0;
		lpDIB = lpDIBorigin + iCol;
		p= lpDIB;

		//find the first  valid point
		if( *p == iFillValue){
			while(*p == iFillValue){  //find the fisrt point with valid value
				iYstart++;
				p += iImgWidth;
				if(iYstart >= iImgHeight)  break;
			}
		}

		//now p point has value; iYStart

		while(iYstart < iImgHeight) {
			while(*p != iFillValue){  //find the fisrt point with invalid value
				iYstart++;
				p += iImgWidth;
				if(iYstart >= iImgHeight)  break;

			}

			if(iYstart < iImgHeight) {
				iYend =iYstart ;
				iYstart--;

				while(*p == iFillValue){  //find the fisrt point with invalid value
					iYend++;
					p += iImgWidth;
					if(iYend >= iImgHeight)  break;
				}
				if(iYend < iImgHeight){

					//interpolate the points between iYstart and iYend
					if(iInputType == 0 ){ // WORD
						dV2 = (double)(*p) /(double)(iYend-iYstart);
						p = lpDIB + iYstart * iImgWidth ;
						dV1 = (double)(*p) /(double)(iYend-iYstart);
						for(iRow =iYstart +1; iRow <iYend; iRow++){
							p += iImgWidth;
							if(*p != iBadData ) *p = (int)(dV2 *(iRow - iYstart) + dV1 *(iYend -iRow));
						}
					}else{ //short int
						short int n;
						n= (short int)(*p);
						dV2 = (double)(n) /(double)(iYend-iYstart);
						p = lpDIB + iYstart * iImgWidth ;
						n= (short int)(*p);
						dV1 = (double)(n) /(double)(iYend-iYstart);
						for(iRow =iYstart +1; iRow <iYend; iRow++){
							p += iImgWidth;
							n = (int)(dV2 *(iRow - iYstart) + dV1 *(iYend -iRow));
							if(( short)(*p) != iBadData ) *p =(short)n;
						}
					}
				}

				iYstart =iYend;
				p = lpDIB + iYstart * iImgWidth ;

			}else
				break;
		}


	}//loop: iCol


}


void CFill_Gap_By_InterpolatingAlongX(unsigned short *lpDIBorigin, int iImgWidth, int iImgHeight, int iInputType, short iFillValue, short iBadData)
{
    if(lpDIBorigin == NULL) return ;   //DIB has not been allocated
	long iCol,  iRow;
	long iXstart,iXend;
	double dV1,dV2;
	short *lpDIB = lpDIBorigin ;
	short *p;
	for( iRow= 0 ; iRow < iImgHeight; iRow++){


		iXstart=0;
		lpDIB = lpDIBorigin + iRow * iImgWidth;
		p= lpDIB;

		//find the first  valid point
		if( *p == iFillValue){
			while(*p == iFillValue){  //find the fisrt point with valid value
				iXstart++;
				p++;
				if(iXstart >= iImgWidth)  break;
			}
		}

		//now p point has value; iYStart

		while(iXstart < iImgWidth) {
			while(*p != iFillValue){  //find the fisrt point with invalid value
				iXstart++;
				p++;
				if(iXstart >= iImgWidth)  break;
			}

			if(iXstart < iImgWidth) {
				iXend =iXstart ;
				iXstart--;

				while(*p == iFillValue){  //find the fisrt point with invalid value
					iXend++;
					p++;
					if(iXend >= iImgWidth)  break;
				}
				if(iXend < iImgWidth){

					//interpolate the points between iXstart and iXend
					if(iInputType == 0 ){ // WORD
						dV2 = (double)(*p) / (double)(iXend-iXstart);
						p = lpDIB +  iXstart;
						dV1 = (double)(*p) /(double)(iXend-iXstart);
						for(iCol =iXstart +1; iCol <iXend; iCol++){
							p ++;
							if(*p != iBadData ) *p = (int)(dV2 *(iCol - iXstart) + dV1 *(iXend -iCol));
						}
					}else{ //short int
						short int n;
						n= (short int)(*p);
						dV2 = (double)(n) /(double)(iXend-iXstart);
						p = lpDIB + iXstart;
						n= (short int)(*p);
						dV1 = (double)(n) /(double)(iXend-iXstart);
						for(iCol =iXstart +1; iCol <iXend; iCol++){
							p ++;
							n = (int)(dV2 *(iCol - iXstart) + dV1 *(iXend -iCol));
							if((short)(*p) != iBadData ) *p = (short)n;
						}
					}
				}

				iXstart =iXend;
				p = lpDIB +  iXstart;

			}else
				break;
		}


	}//loop: iCol

}