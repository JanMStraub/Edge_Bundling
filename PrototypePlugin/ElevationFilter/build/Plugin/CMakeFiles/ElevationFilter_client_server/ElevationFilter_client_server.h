#ifndef ElevationFilter_client_server_h
#define ElevationFilter_client_server_h

#include "vtkClientServerInterpreter.h"

extern "C" void ElevationFiltersCS_Initialize(vtkClientServerInterpreter*);

inline void ElevationFilter_client_server_initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  ElevationFiltersCS_Initialize(csi);
}

#endif
