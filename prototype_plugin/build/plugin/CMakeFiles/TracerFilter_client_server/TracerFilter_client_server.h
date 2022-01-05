#ifndef TracerFilter_client_server_h
#define TracerFilter_client_server_h

#include "vtkClientServerInterpreter.h"

extern "C" void TracerFiltersCS_Initialize(vtkClientServerInterpreter*);

inline void TracerFilter_client_server_initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  TracerFiltersCS_Initialize(csi);
}

#endif
