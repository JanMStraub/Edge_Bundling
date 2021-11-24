#include "vtkCPPFilter.h"
#include "vtkObjectFactory.h"
#include <QMessageBox>

vtkStandardNewMacro(vtkCPPFilter);

vtkCPPFilter::vtkCPPFilter() {}

vtkCPPFilter::~vtkCPPFilter() {}

void vtkCPPFilter::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os,indent);
}

// Method that creates a variable for Python using SetParameter
void vtkCPPFilter::SetSizz(double value)
{
	/*
	char s[255];
	sprintf(s, "SetSizz was invoked %f\n", value);
	QMessageBox::information(NULL, "MyAction", s);
	*/

	// Create a new variable for Python called 'sizz'
	SetParameter("sizz", value);
}