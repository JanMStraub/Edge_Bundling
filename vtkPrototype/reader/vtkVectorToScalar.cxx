#include <string>
#include <iostream>
#include <algorithm>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkUnstructuredGrid.h>
#include <vtkFloatArray.h>
#include <vtkNew.h>
#include <vtkPolyData.h>
#include <vtkPointData.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkScalarBarActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkColorTransferFunction.h>

int main () {

    std::cout << "Program start" << std::endl;

    std::string inputFilename = "/Users/jan/Google Drive/Programmieren/bachelor_thesis/vtkPrototype/data/tmp_3D.vtk";

    // Read input file 
    vtkNew<vtkUnstructuredGridReader> reader;
    reader->SetFileName(inputFilename.c_str());
    reader->Update();

    vtkUnstructuredGrid* output = reader->GetOutput();

    int numberOfPoints = output->GetNumberOfPoints();

    std::cout << "Number of points: " << numberOfPoints << std::endl;

    // Calculate scalars 
    vtkNew<vtkFloatArray> scalars;
    scalars->SetNumberOfValues(numberOfPoints);

    double min = 0;
    double max = 0;

    for (int i = 0; i < numberOfPoints; ++i) {
        scalars->SetValue(i, static_cast<float>(i) / numberOfPoints);

        // Just for color calculation
        if (scalars->GetValue(i) > max) {
            max = scalars->GetValue(i);
        } else if (scalars->GetValue(i) < min) {
            min = scalars->GetValue(i);
        }
    }

    std::cout << "Max: " << max << std::endl;
    std::cout << "Min: " << min << std::endl;
    
    vtkNew<vtkPolyData> poly;
    poly->DeepCopy(output);
    poly->GetPointData()->SetScalars(scalars);

    vtkNew<vtkVertexGlyphFilter> vertexGlyphFilter;
    vertexGlyphFilter->SetInputData(poly);

    vtkNew<vtkPolyDataMapper> signedDistanceMapper;
    signedDistanceMapper->SetInputConnection(vertexGlyphFilter->GetOutputPort());
    signedDistanceMapper->ScalarVisibilityOn();

    // Color
    double colors[5][3] = { { 0, 0, 1},
                            { 0, 0.5, 0.5 },
                            { 0, 1, 0 },
                            { 0.5, 0.5, 0 },
                            { 1, 0, 0 } };

    vtkNew<vtkColorTransferFunction> colorFunction;
    colorFunction->SetUseBelowRangeColor( true );
    colorFunction->SetBelowRangeColor( colors[0] );
    colorFunction->SetNanColor( colors[0] );
    colorFunction->AddRGBPoint( 0, colors[0][0], colors[0][1], colors[0][2] );
    colorFunction->AddRGBPoint( 0.3, colors[1][0], colors[1][1], colors[1][2] );
    colorFunction->AddRGBPoint( 0.5, colors[2][0], colors[2][1], colors[2][2] );
    colorFunction->AddRGBPoint( 0.8, colors[3][0], colors[3][1], colors[3][2] );
    colorFunction->AddRGBPoint( 1, colors[4][0], colors[4][1], colors[4][2] );
    colorFunction->Build();

    signedDistanceMapper->SetLookupTable( colorFunction );
    signedDistanceMapper->UseLookupTableScalarRangeOn();

    vtkNew<vtkActor> signedDistanceActor;
    signedDistanceActor->SetMapper(signedDistanceMapper);

    vtkNew<vtkRenderer> renderer;
    renderer->AddViewProp(signedDistanceActor);

    vtkNew<vtkRenderWindow> renderWindow;
    renderWindow->AddRenderer(renderer);

    vtkNew<vtkRenderWindowInteractor> renWinInteractor;
    renWinInteractor->SetRenderWindow(renderWindow);

    renderWindow->Render();
    renWinInteractor->Start();

    std::cout << "Program finished" << std::endl;

    return EXIT_SUCCESS;
}