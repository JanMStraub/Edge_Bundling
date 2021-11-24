#ifndef __vtkMyElevationFilter_h
#define __vtkMyElevationFilter_h

#include "vtkPythonProgrammableFilter.h"

class VTK_EXPORT vtkCPPFilter : public vtkPythonProgrammableFilter
{
	public:
		static vtkCPPFilter* New();
		vtkTypeMacro(vtkCPPFilter, vtkPythonProgrammableFilter);
		void PrintSelf(ostream& os, vtkIndent indent);
  
		// Method that creates a variable for Python using SetParameter
		void SetSizz(double);

	protected:
		vtkCPPFilter();
		~vtkCPPFilter();

	private:
		vtkCPPFilter(const vtkCPPFilter&);  // Not implemented.
		void operator=(const vtkCPPFilter&);  // Not implemented.
};

#endif