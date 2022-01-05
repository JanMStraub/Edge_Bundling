#include "vtkABI.h"
#include "vtkClientServerInterpreter.h"

extern void vtkMyStreamTracerFilter_Init(vtkClientServerInterpreter*);
extern void StreamTracerFiltersModule_Init(vtkClientServerInterpreter*);

extern "C" void VTK_ABI_EXPORT StreamTracerFiltersCS_Initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  vtkMyStreamTracerFilter_Init(csi);
  StreamTracerFiltersModule_Init(csi);
}
