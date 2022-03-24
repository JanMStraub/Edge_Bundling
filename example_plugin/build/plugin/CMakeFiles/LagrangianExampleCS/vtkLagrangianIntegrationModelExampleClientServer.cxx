// ClientServer wrapper for vtkLagrangianIntegrationModelExample object
//
#define VTK_WRAPPING_CXX
#define VTK_STREAMS_FWD_ONLY
#include "vtkLagrangianIntegrationModelExample.h"
#include "vtkSystemIncludes.h"
#include "vtkClientServerInterpreter.h"
#include "vtkClientServerStream.h"


vtkObjectBase *vtkLagrangianIntegrationModelExampleClientServerNewCommand(void* /*ctx*/)
{
  return vtkLagrangianIntegrationModelExample::New();
}


int VTK_EXPORT vtkLagrangianIntegrationModelExampleCommand(
  vtkClientServerInterpreter *arlu, vtkObjectBase *ob,
  const char *method, const vtkClientServerStream& msg,
  vtkClientServerStream& resultStream, void* /*ctx*/)
{
  vtkLagrangianIntegrationModelExample *op = vtkLagrangianIntegrationModelExample::SafeDownCast(ob);
  if(!op)
    {
    vtkOStrStreamWrapper vtkmsg;
    vtkmsg << "Cannot cast " << ob->GetClassName() << " object to vtkLagrangianIntegrationModelExample.  "
           << "This probably means the class specifies the incorrect superclass in vtkTypeMacro.";
    resultStream.Reset();
    resultStream << vtkClientServerStream::Error
                 << vtkmsg.str() << 0 << vtkClientServerStream::End;
    return 0;
    }
  (void)arlu;
  if (!strcmp("IsTypeOf",method) && msg.GetNumberOfArguments(0) == 3)
    {
    char    *temp0;
    int      temp20;
    if(msg.GetArgument(0, 2, &temp0))
      {
      temp20 = vtkLagrangianIntegrationModelExample::IsTypeOf(temp0);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("IsA",method) && msg.GetNumberOfArguments(0) == 3)
    {
    char    *temp0;
    int      temp20;
    if(msg.GetArgument(0, 2, &temp0))
      {
      temp20 = (op)->IsA(temp0);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("SafeDownCast",method) && msg.GetNumberOfArguments(0) == 3)
    {
    vtkObjectBase  *temp0;
    vtkLagrangianIntegrationModelExample  *temp20;
    if(vtkClientServerStreamGetArgumentObject(msg, 0, 2, &temp0, "vtkObjectBase"))
      {
      temp20 = vtkLagrangianIntegrationModelExample::SafeDownCast(temp0);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << (vtkObjectBase *)temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("NewInstance",method) && msg.GetNumberOfArguments(0) == 2)
    {
    vtkLagrangianIntegrationModelExample  *temp20;
      {
      temp20 = (op)->NewInstance();
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << (vtkObjectBase *)temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("GetNumberOfGenerationsFromBaseType",method) && msg.GetNumberOfArguments(0) == 3)
    {
    char    *temp0;
    long long   temp20;
    if(msg.GetArgument(0, 2, &temp0))
      {
      temp20 = vtkLagrangianIntegrationModelExample::GetNumberOfGenerationsFromBaseType(temp0);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("GetNumberOfGenerationsFromBase",method) && msg.GetNumberOfArguments(0) == 3)
    {
    char    *temp0;
    long long   temp20;
    if(msg.GetArgument(0, 2, &temp0))
      {
      temp20 = (op)->GetNumberOfGenerationsFromBase(temp0);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("New",method) && msg.GetNumberOfArguments(0) == 2)
    {
    vtkLagrangianIntegrationModelExample  *temp20;
      {
      temp20 = vtkLagrangianIntegrationModelExample::New();
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << (vtkObjectBase *)temp20 << vtkClientServerStream::End;
      return 1;
      }
    }
  if (!strcmp("InitializeParticleData",method) && msg.GetNumberOfArguments(0) == 4)
    {
    vtkFieldData  *temp0;
    int      temp1;
    if(vtkClientServerStreamGetArgumentObject(msg, 0, 2, &temp0, "vtkFieldData") &&
      msg.GetArgument(0, 3, &temp1))
      {
      op->InitializeParticleData(temp0,temp1);
      return 1;
      }
    }
  if (!strcmp("ComputeSurfaceDefaultValues",method) && msg.GetNumberOfArguments(0) == 6)
    {
    char    *temp0;
    vtkDataSet  *temp1;
    int      temp2;
    vtkClientServerStreamDataArg<double > temp3(msg, 0, 5);
    if(msg.GetArgument(0, 2, &temp0) &&
      vtkClientServerStreamGetArgumentObject(msg, 0, 3, &temp1, "vtkDataSet") &&
      msg.GetArgument(0, 4, &temp2) &&
      temp3)
      {
      op->ComputeSurfaceDefaultValues(temp0,temp1,temp2,temp3);
      return 1;
      }
    }
  if (!strcmp("FunctionValues",method) && msg.GetNumberOfArguments(0) == 4)
    {
    vtkClientServerStreamDataArg<double > temp0(msg, 0, 2);
    vtkClientServerStreamDataArg<double > temp1(msg, 0, 3);
    int      temp20;
    if(temp0 &&
      temp1)
      {
      temp20 = (op)->FunctionValues(temp0,temp1);
      resultStream.Reset();
      resultStream << vtkClientServerStream::Reply << temp20 << vtkClientServerStream::End;
      return 1;
      }
    }

  {
    const char* commandName = "vtkLagrangianBasicIntegrationModel";
    if (arlu->HasCommandFunction(commandName) &&
        arlu->CallCommandFunction(commandName, op, method, msg, resultStream)) { return 1; }
  }
  if(resultStream.GetNumberOfMessages() > 0 &&
     resultStream.GetCommand(0) == vtkClientServerStream::Error &&
     resultStream.GetNumberOfArguments(0) > 1)
    {
    /* A superclass wrapper prepared a special message. */
    return 0;
    }
  vtkOStrStreamWrapper vtkmsg;
  vtkmsg << "Object type: vtkLagrangianIntegrationModelExample, could not find requested method: \""
         << method << "\"\nor the method was called with incorrect arguments.\n";
  resultStream.Reset();
  resultStream << vtkClientServerStream::Error
               << vtkmsg.str() << vtkClientServerStream::End;
  vtkmsg.rdbuf()->freeze(0);
  return 0;
}


//-------------------------------------------------------------------------auto
void VTK_EXPORT vtkLagrangianIntegrationModelExample_Init(vtkClientServerInterpreter* csi)
{
  static vtkClientServerInterpreter* last = nullptr;
  if(last != csi)
    {
    last = csi;
    csi->AddNewInstanceFunction("vtkLagrangianIntegrationModelExample", vtkLagrangianIntegrationModelExampleClientServerNewCommand);
    csi->AddCommandFunction("vtkLagrangianIntegrationModelExample", vtkLagrangianIntegrationModelExampleCommand);
    }
}
