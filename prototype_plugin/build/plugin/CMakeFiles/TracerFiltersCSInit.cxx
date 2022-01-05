#include "vtkABI.h"
#include "vtkClientServerInterpreter.h"

extern void vtkMyTracerFilter_Init(vtkClientServerInterpreter*);
extern void TracerFiltersModule_Init(vtkClientServerInterpreter*);

extern "C" void VTK_ABI_EXPORT TracerFiltersCS_Initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  vtkMyTracerFilter_Init(csi);
  TracerFiltersModule_Init(csi);
}
