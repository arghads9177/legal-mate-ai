#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.text_validator.text_validator_crew import TextValidatorCrew
from crews.legal_summarizer.legal_summarizer_crew import LegalMateAi
import json


class LegalTextState(BaseModel):
    is_valid: bool = False
    contract_text: str = ""
    contract_summary: str = ""
    error_message: str = ""


class LegalContractSummerizerFlow(Flow[LegalTextState]):

    def set_contract_text(self, contract_text: str = ""):
        print("Setting contract text")
        self.state.contract_text = contract_text

    def get_response(self):
        if self.state.is_valid:
            return self.state.contract_summary
        else:
            return self.state.error_message

    @start()
    def validate_contract_text(self):
        print("Validating contract text")
        result = (
            TextValidatorCrew()
            .crew()
            .kickoff(inputs={"contract_text": self.state.contract_text})
        )

        print("Validation result", result.raw)
        # Parse the raw string as JSON
        try:
            parsed_result = json.loads(result.raw)
            self.state.is_valid = parsed_result.get("is_valid", False)
        except json.JSONDecodeError:
            print("Error: Could not parse JSON from result.raw")
            self.state.is_valid = False
    
    @listen(validate_contract_text)
    def summarize_contract_text(self):
        if self.state.is_valid:
            print('Summarizing contract text')
            result = (
                LegalMateAi()
                .crew()
                .kickoff(inputs={"contract_text": self.state.contract_text})
            )
            print("Summarization result", result.raw)
            self.state.contract_summary = result.raw
        else:
            self.state.error_message = "❌ The provided input does not appear to be a legal contract. Please upload or paste a valid contract document to proceed."
            print('❌ The provided input does not appear to be a legal contract. Please upload or paste a valid contract document to proceed.')
            return

def kickoff(contract_text: str = ""):
    lcs_flow = LegalContractSummerizerFlow()
    lcs_flow.set_contract_text(contract_text)
    lcs_flow.kickoff()
    return lcs_flow.get_response()


def plot():
    lcs_flow = LegalContractSummerizerFlow()
    lcs_flow.plot()

invalid_contract_input = """
Project : “System Driven Logistics Forecast Module to Generate Cost-Optimal Vessel Scheduling and Port Plant Linkages with AIIntervention’’:


    a. Present Scheme of arrangements : (The flow diagram attached in Annexure A)SAIL owns and operates five Integrated Steel Plants at Bhilai, Rourkela, Durgapur, Bokaro and Burnpur. With Hot Metal capacity of 19.3 MMT, the present imported coal and limestone consumption is approx. 17.3 MMTand 3 MMT respectively. The imported coal and lime stone is procured from offshore countries like Australia ,USA,Indonesia,Mozambique & Russia(for coal) and UAE (forLime stone). SAIL vesselsare normally lightened at the first port and it then sails to the second port of call ( normallyHaldia ) for completion of discharge. Generally the first port of discharge for a Panamax / Handymax vessel is Vizag, Gangavaram, Paradip, Dhamra and Sandheads. Haldia being a riverine port, vessels need to be lightened at the first port and can then be completed at this port. SAIL also handles Cape vessels at Dhamra, Gangavaram, Sandheads/ Saguor. Further Haldia being the nearest port from all eastern sector Steel Plants of SAIL, its advantageous w.r.t Railway freight and empty generation. 
Coal Import Group, Delhi arranges procurement of metallurgical imported coal of SAIL, while Central Materials Management Group, Delhi arranges same for imported limestone. This translates into annual import plan of imported coal and limestone, which is then finalized on quarterly basis with various coal/limestone Suppliers. Thereafter the Supplier-wise shipments is conveyed to Transport and Shipping in the form of STEM which defines a particular quality from a Supplier, parcel size, loadport and laydays. T&S then undertakes Chartering for finalizing vessels against the STEMS received. Inputs pertaining to a particular STEM, vessel nomination against the STEM laydays, sailing of the vessel, receipt of cargo at ports, despatch from port and the statutory and non-statutory payments related to a particular vessel are mapped in the existing SAP system. 
Operations Directorate, Delhi conveys a quality-wise, plant-wise monthly despatch plan to T&S. T&S chalks out a port-plant linkage on the basis of total coal availability, by plotting the coal stocks available at ports, receipts in incoming vessels, certain pre-defined port-wise/ location specific constraintsagainst the dispatch requirement received from Opr. Dte.
The same scheme of things is is followed forimported limestone also.
    1. 
    b. Objective of the Proposed AIDriven Project:

The logistics function drives the planning and cost management of the end-to-end supply chain. Considering the nature of operations at steel plant and the market dynamics, the logistics team manages the complex trade-offs to maintain production continuity, avoid stock-outs, optimize inventory carrying costs, overcome location specific constraints, ship/ rake availability, etc.The proposed digital platform will utilise the analytics-driven tools and processes to drive the logistics planning/scheduling within the given constraints and optimize the performance as well as the cost of logistics (“Project”)and integrate same withSAIL’s SAP system.


    c. Scope of The Proposed Project Work
.
The overall Project shall be delivered through the following stages – 

Stage 1: 	
1.	Phase 1- Baseline and analysis (3 months)
2.	Phase 2- Benchmarking (1 month)
3.	Phase 3- Logistics solution design (4 months)
4.	Phase 4- Implementation support for solution delivery (4 months)

The detailed scope for Stage 1 is as follows - 
Phase 1: Baseline and analysis (3 months) 
1.	Map SAIL’s overall production including hot metal and saleable steel/iron production for FY22-23 (“FY23”). This shall cover all steel plants. The future expansion plan also need to be taken into consideration for scalability of the project.

2.	Assess the input material movement, including but not limited to –
a.	Imports mapping: Current sources for imports, tonnage movement across ports including O-D pairs, vessels used for movement, the freight paid, terms of freight charges, lead time for destination port, agents/ organization structure managing inbound logistics at source locations, quality control checks, policies/ processes/ certifications driving the costs, technology deployed for materials management, constraints at ports and delivery performance.

b.	Port to plant logistics: Map and analyze the process/tools used for defining port-plant linkages, tonnage movement between ports and plants, the freight paid, terms of freight charges, the lead time required for such movement, rake handling time at ports and plants, technology deployed, constraints at ports/ plants and delivery performance. The consultant shall visit and study the constraints at the domestic ports and plants.

The Consultant shall visit and study the constraints at the all integrated steel plants at Bhilai, Bokaro, Rourkela, Durgapur, Burnpur


3.	Overall governance process for driving logistics function across SAIL – The consultant shall map areas such as – 
a.	Organization structure for inbound and outbound logistics
b.	Processes followed for governance – including the KPIs monitored and review system
c.	Infrastructure planning and resolution of constraints at port/ plant.	Stakeholders involved in resolution of the constraints
e.	Investment and other operational initiatives planned for resolving the constraints

4.	Prepare baseline of KPIs (Key Performance Indicators) across supply chain nodes such as load ports, discharge ports and plants. The baseline shall cover sufficient timelines to meaningfully draw inferences or 12 months, whichever is higher. The Consultant shall also assess SAIL’s current methodology/ definitions to capture these KPIs.

5.	The Consultant shall analyze the baseline prepared and articulate the key gap areas for SAIL.

Phase 2:
Benchmarking (1 month)
The consultant shall analyze 2-3 benchmarks within Steel industry from global as well as domestic standpoint. The Consultant shall apply own understanding of the industry and SAIL’s baseline to synthesize further learnings for SAIL. 

Phase 3:
Logistics solution design (4 months)
The consultant shall define the overall logistics transformation from the following aspects – 

    1. Analytics driven model for supply chain planning – the model shall define achievable targets for order fulfillment and cost parameters, amongst the other.
    2. Process changes required to effectively roll out the tool/ analytical model deployment
    3. Solutions for resolving the key constraints across supply chain nodes such as ports, plants and mines
    4. Key elements of governance model


Expected Outcome/Benefits form implementation of the Project :

Following are the details to be achieved through AI logistics solution design :

1.	Analytics driven model for supply chain planning:
    a. Optimal operating ranges for the key decision parameters controllable by logistics function. The tool must factor in the key operating restrictions to drive high level of predictive accuracy for the range of input parameters. 
    b. Visibility : The model should show visibility across the logistics nodes, visibility of vessels at Load Port ,en-route & at discharge Port,  loaded Railways Rakes from Ports till unloading at recipient points with details tagged  across the flow.
    c. The Consultant shall apply their business understanding to define the opportunity costs as well as other areas to define the ‘costs’ as the effect of choice of the input/ decision parameters
    d. Identification of broad operating ranges across key set of supply chain nodes for the given commodities under routine operating conditions. The broad operating ranges shall be converted to SOP (Standard Operating Procedures) for the day to day usage
    e. The analytical model shall recommend vessel scheduling and port-port linkages (imports), along with the key parameters for planning and costs. 
    f. The analytics driven model/ tool shall be scalable for SAIL’s future usage keeping in view the planned expansion .

2.	Process changes required to effectively roll out the tool/ analytical model deployment: The Consultant shall recommend process changes required to effectively achieve optimal operating conditions as per the tool’s recommendations. 


Phase 4: Time line for Implementation support for solution delivery (4 months)
The consultant shall assist in rolling out of the solution including analytical model, process changes, resolving constraints and institutionalizing right governance model. The support shall include areas such as- 

    a. Testing of analytical model using real world data
    b. Troubleshooting and refinements in the model
    c. Training for master users
    d. Transfer of model/ tool on SAIL server, as the need be
    e. Deployment of pilot processes across select plants/ ports
    f. Preparation of select capex proposals including cost-benefit analysis for resolving the key constraints requiring investments
    g. Hand-holding SAIL teams to resolve operational practices
    h. Hand-holding SAIL teams to define scenarios, conduct interpretation, check whether / how the optimal input conditions can be achieved and how to opt for ‘next best’ scenario
    i. Ongoing correction of predictive operating accuracy of the analytical model
    j. Tracking mechanism for inability to adopt the most optimal models across a set interval of inbound/ outbound trips. A report shall be generated covering the ‘deviation from optimal’ and the resultant impact on the cost. The report shall be shared with SAIL’s functional Heads.





"""

valid_contract_input = """
Sample Legal Contract – Complex Version with Subclauses
SERVICE AGREEMENT
This Service Agreement ("Agreement") is made effective as of March 15, 2024, by and between:

AlphaTech Solutions Pvt. Ltd., a company incorporated under the Companies Act, 2013 having its registered office at 102/A, Technopark, Bengaluru, India – 560100, hereinafter referred to as the “Service Provider”.

NeoFin Bank Inc., a Delaware corporation with its principal place of business at 45 Wall Street, New York, NY, USA – 10005, hereinafter referred to as the “Client”.

1. Scope of Services
The Service Provider agrees to perform the following services:
1.1 Develop and maintain a cloud-based fraud detection platform.
1.2 Integrate the platform with Client’s banking APIs.
1.3 Conduct quarterly audits and compliance checks.
1.4 Provide 24/7 technical support through a designated team.

2. Term and Termination
2.1 The Agreement shall commence on March 15, 2024, and continue for a term of 24 months unless terminated earlier as per this clause.
2.2 Either party may terminate this Agreement with 90 days’ written notice.
2.3 The Client may terminate the Agreement immediately upon:

(a) Any material breach not remedied within 30 days of notice.

(b) Insolvency or bankruptcy of the Service Provider.

(c) Failure to meet KPIs in two consecutive quarters.

3. Payment Terms
3.1 The Client shall pay the Service Provider USD 150,000 per quarter.
3.2 Payment shall be made within 30 days of invoice receipt.
3.3 Late payments beyond 15 days shall attract an interest of 2% per month.
3.4 All fees are exclusive of applicable taxes.

4. Performance and Delivery Milestones
4.1 Initial Platform Deployment – May 30, 2024
4.2 Phase 2 Feature Release – October 15, 2024
4.3 Security Certification Audit – February 10, 2025
4.4 Final Review & Renewal – March 1, 2026

5. Confidentiality
5.1 Each party shall maintain confidentiality of all proprietary or sensitive information.
5.2 Disclosure shall be limited to employees, subcontractors, or agents strictly on a “need-to-know” basis.
5.3 Obligations under this clause survive for 5 years post termination.

6. Limitation of Liability
6.1 Except for wilful misconduct, neither party shall be liable for indirect or consequential damages.
6.2 The total cumulative liability shall not exceed the total fees paid in the previous 12 months.

7. Dispute Resolution
7.1 Any dispute shall first be resolved through good faith negotiation between senior executives.
7.2 Failing that, the matter shall be referred to binding arbitration under ICC Rules in Singapore.
7.3 Each party shall bear its own arbitration costs unless otherwise awarded by the tribunal.

8. Governing Law
This Agreement shall be governed by and construed in accordance with the laws of Singapore, without regard to its conflict of law principles.

9. Miscellaneous
9.1 This Agreement constitutes the entire agreement and supersedes prior discussions.
9.2 Modifications shall be in writing and signed by authorized representatives.
9.3 Notices must be sent via registered email or courier to official addresses.

IN WITNESS WHEREOF, the parties hereto have executed this Agreement.

Signatures
AlphaTech Solutions Pvt. Ltd.
Name: Rakesh Menon
Designation: Director of Engineering

NeoFin Bank Inc.
Name: Samantha Goldstein
Designation: VP, Vendor Partnerships
"""

# if __name__ == "__main__":
#     result = kickoff(contract_text=valid_contract_input)
#     print("Final Result:", result)
