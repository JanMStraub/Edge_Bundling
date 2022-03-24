#ifndef LagrangianIntegrationModel_client_server_h
#define LagrangianIntegrationModel_client_server_h

#include "vtkClientServerInterpreter.h"

extern "C" void LagrangianExampleCS_Initialize(vtkClientServerInterpreter*);

inline void LagrangianIntegrationModel_client_server_initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  LagrangianExampleCS_Initialize(csi);
}

#endif
