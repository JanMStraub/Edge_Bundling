<xml>
<proxy>
    <group>filters</group>
    <name>MyElevationFilter</name>
    <label>MyElevation</label>
    <documentation>
        <brief>Create point attribute array by projecting points onto an elevation vector.</brief>
        <long>
          The Elevation filter generates point scalar values for an input data
          set along a specified direction vector. The Input menu allows the user
          to select the data set to which this filter will be applied. The Low
          Point and High Point define a line onto which each point of the data
          set is projected. The minimum scalar value is associated with the Low
          Point, and the maximum scalar value is associated with the High Point.
          The scalar value for each point in the data set is determined by the
          location along the line to which that point projects.

          The line can be specified interactively using the 3D line widget. See
          section 7.4 for more information about this widget.
     </long>
    </documentation>
    <property>
        <name>Input</name>
        <label>Input</label>
        <defaults/>
        <domains>
            <domain>
                <text>Accepts input of following types:</text>
                <list>
                    <item>vtkDataSet</item>
                </list>
            </domain>
        </domains>
    </property>
    <property>
        <name>LowPoint</name>
        <label>Low Point</label>
        <documentation>
            <brief/>
            <long>
           Define one end of the line (small scalar values). Default is (0,0,0).
         </long>
        </documentation>
        <defaults>0 0 0</defaults>
        <domains>
            <domain>
                <text>
      The value must lie within the bounding box of the dataset.
      
        It will default to the min in each dimension.
      </text>
            </domain>
        </domains>
    </property>
    <property>
        <name>HighPoint</name>
        <label>High Point</label>
        <documentation>
            <brief/>
            <long>
           Define other end of the line (large scalar values). Default is (0,0,1).
         </long>
        </documentation>
        <defaults>0 0 1</defaults>
        <domains>
            <domain>
                <text>
      The value must lie within the bounding box of the dataset.
      
        It will default to the max in each dimension.
      </text>
            </domain>
        </domains>
    </property>
</proxy>

</xml>
