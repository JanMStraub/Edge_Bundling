#include "vtkABI.h"
#include "vtkClientServerInterpreter.h"

extern void vtkLagrangianIntegrationModelExample_Init(vtkClientServerInterpreter*);
extern void LagrangianExampleModule_Init(vtkClientServerInterpreter*);

extern "C" void VTK_ABI_EXPORT LagrangianExampleCS_Initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  vtkLagrangianIntegrationModelExample_Init(csi);
  LagrangianExampleModule_Init(csi);
}
