#!/bin/bash

# Script para gerar planos de carga apenas para interface SAS-SAS (WINNF TS-0096/3003)

echo "🔧 Gerando planos de carga para SAS-SAS (WINNF TS-0096/3003)"
echo "=============================================================="
echo ""

# Lista de endpoints SAS-SAS
ENDPOINTS=("cbsd_get" "cbsd_post" "zone_get" "zone_post" "dump_get")
LEVELS=("low" "medium" "high" "stress" "endurance")

# Configurações por nível
declare -A CONFIG
CONFIG[low_threads]="2"
CONFIG[low_loops]="5"
CONFIG[low_ramp]="10"
CONFIG[medium_threads]="5"
CONFIG[medium_loops]="10"
CONFIG[medium_ramp]="20"
CONFIG[high_threads]="15"
CONFIG[high_loops]="20"
CONFIG[high_ramp]="45"
CONFIG[stress_threads]="30"
CONFIG[stress_loops]="30"
CONFIG[stress_ramp]="90"
CONFIG[endurance_threads]="10"
CONFIG[endurance_loops]="50"
CONFIG[endurance_ramp]="60"
CONFIG[endurance_duration]="1800"

# Função para gerar plano
generate_plan() {
    local endpoint=$1
    local level=$2
    local filename="sas_sas_${endpoint}_${level}.jmx"
    local threads=${CONFIG[${level}_threads]}
    local loops=${CONFIG[${level}_loops]}
    local ramp=${CONFIG[${level}_ramp]}
    local duration=${CONFIG[${level}_duration]:-""}
    local api_path=""
    local payload=""
    local method="GET"
    local testname=""

    case $endpoint in
        "cbsd_get")
            api_path="/v1.3/cbsd/TEST-SN-001"
            method="GET"
            testname="CBSD GET"
            ;;
        "cbsd_post")
            api_path="/v1.3/cbsd/TEST-SN-001"
            method="POST"
            payload='{"id":"TEST-SN-001","fccId":"TEST-FCC-001","userId":"TEST-USER-001","cbsdSerialNumber":"TEST-SN-001","callSign":"TESTCALL","cbsdCategory":"A","airInterface":"E_UTRA","measCapability":["EUTRA_CARRIER_RSSI"],"eirpCapability":47,"latitude":375000000,"longitude":1224000000,"height":30,"heightType":"AGL","indoorDeployment":false,"antennaGain":15,"antennaBeamwidth":360,"antennaAzimuth":0,"groupingParam":"","cbsdAddress":"0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"}'
            testname="CBSD POST"
            ;;
        "zone_get")
            api_path="/v1.3/zone/ZONE-001"
            method="GET"
            testname="Zone GET"
            ;;
        "zone_post")
            api_path="/v1.3/zone/ZONE-001"
            method="POST"
            payload='{"id":"ZONE-001","name":"Zone Example","type":"protected","geometry":{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}}'
            testname="Zone POST"
            ;;
        "dump_get")
            api_path="/v1.3/dump"
            method="GET"
            testname="Dump GET"
            ;;
    esac

    echo "🔧 Gerando: $filename"

    cat > "../plans/$filename" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="SAS-SAS ${testname} - Carga ${level^}" enabled="true">
      <stringProp name="TestPlan.comments">Benchmark SAS-SAS ${testname} com carga ${level} (${threads} usuários, ${loops} iterações)</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.arguments" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="${testname} Thread Group - ${level^}" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">${loops}</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">${threads}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">${ramp}</stringProp>
        <boolProp name="ThreadGroup.scheduler">${duration:+true}</boolProp>
        <stringProp name="ThreadGroup.duration">${duration}</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="${testname} SAS-SAS" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
            <collectionProp name="Arguments.arguments">
EOF

    if [ "$method" = "POST" ] && [ -n "$payload" ]; then
        cat >> "../plans/$filename" << EOF
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">${payload}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
EOF
    fi

    cat >> "../plans/$filename" << EOF
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">localhost</stringProp>
          <stringProp name="HTTPSampler.port">8000</stringProp>
          <stringProp name="HTTPSampler.protocol">http</stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">${api_path}</stringProp>
          <stringProp name="HTTPSampler.method">${method}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>
        <hashTree>
EOF

    if [ "$method" = "POST" ]; then
        cat >> "../plans/$filename" << EOF
          <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP Header Manager" enabled="true">
            <collectionProp name="HeaderManager.headers">
              <elementProp name="" elementType="Header">
                <stringProp name="Header.name">Content-Type</stringProp>
                <stringProp name="Header.value">application/json</stringProp>
              </elementProp>
            </collectionProp>
          </HeaderManager>
          <hashTree/>
EOF
    fi

    cat >> "../plans/$filename" << EOF
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="Response Code Assertion" enabled="true">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="49586">200</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">8</intProp>
          </ResponseAssertion>
          <hashTree/>
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
EOF

    echo "✅ $filename gerado com sucesso"
}

# Gerar todos os planos
mkdir -p ../plans
for endpoint in "${ENDPOINTS[@]}"; do
    for level in "${LEVELS[@]}"; do
        generate_plan "$endpoint" "$level"
    done
done

echo ""
echo "🎉 Planos SAS-SAS gerados!"
echo "📁 Veja os arquivos em benchmark/jmeter/plans/"
echo "" 