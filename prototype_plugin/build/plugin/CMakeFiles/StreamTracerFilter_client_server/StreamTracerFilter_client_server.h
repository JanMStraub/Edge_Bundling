#ifndef StreamTracerFilter_client_server_h
#define StreamTracerFilter_client_server_h

#include "vtkClientServerInterpreter.h"

extern "C" void StreamTracerFiltersCS_Initialize(vtkClientServerInterpreter*);

inline void StreamTracerFilter_client_server_initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  StreamTracerFiltersCS_Initialize(csi);
}

#endif
