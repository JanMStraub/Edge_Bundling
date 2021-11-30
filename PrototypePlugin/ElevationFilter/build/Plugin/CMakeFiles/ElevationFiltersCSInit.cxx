#include "vtkABI.h"
#include "vtkClientServerInterpreter.h"

extern void vtkMyElevationFilter_Init(vtkClientServerInterpreter*);
extern void ElevationFiltersModule_Init(vtkClientServerInterpreter*);

extern "C" void VTK_ABI_EXPORT ElevationFiltersCS_Initialize(vtkClientServerInterpreter* csi)
{
  (void)csi;
  vtkMyElevationFilter_Init(csi);
  ElevationFiltersModule_Init(csi);
}
