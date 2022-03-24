<xml>
    <proxy>
        <group>lagrangian_integration_models</group>
        <name>LagrangianIntegrationModelExample</name>
        <label>Integration Model Example</label>
        <property>
            <name>FlowVelocity</name>
            <label>Flow Velocity</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use as flow velocity.</long>
            </documentation>
            <defaults>3;0;0;3;FlowVelocity</defaults>
            <domains>
                <domain>
                    <text>An array of vectors is required.</text>
                </domain>
            </domains>
        </property>
        <property>
            <name>FlowDensity</name>
            <label>Flow Density</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use as flow density.</long>
            </documentation>
            <defaults>4;0;0;3;FlowDensity</defaults>
            <domains>
                <domain>
                    <text>An array of scalars is required.</text>
                </domain>
            </domains>
        </property>
        <property>
            <name>FlowDynamicViscosity</name>
            <label>Flow Dynamic Viscosity</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use as flow dynamic viscosity.</long>
            </documentation>
            <defaults>5;0;0;3;FlowDynamicViscosity</defaults>
            <domains/>
        </property>
        <property>
            <name>Particle Diameter</name>
            <label>ParticleDiameter</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use from seeds as particle diameter.</long>
            </documentation>
            <defaults>6;1;0;0;ParticleDiameter</defaults>
            <domains/>
        </property>
        <property>
            <name>Particle Density</name>
            <label>ParticleDensity</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use from seeds as particle density.</long>
            </documentation>
            <defaults>7;1;0;0;ParticleDensity</defaults>
            <domains/>
        </property>
        <property>
            <name>Gravity Constant</name>
            <label>GravityConstant</label>
            <documentation>
                <brief/>
                <long>This property contains the name of
        the array to use from flow input as gravity constant.</long>
            </documentation>
            <defaults>8;0;0;2;GravityConstant</defaults>
            <domains/>
        </property>
    </proxy>
</xml>
