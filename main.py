from dotenv import load_dotenv
load_dotenv()
from agents.connectivity_agent import connectivity_agent
from agents.personalization_agent import personalization_agent
from agents.layout_agent import layout_agent
from agents.crew_alert_agent import crew_alert_agent
from rich import print
from rich.panel import Panel

def main():
    # ====== Step 1: Connectivity Check ======
    print("[bold cyan]\n📡 STEP 1: Checking Connectivity...[/bold cyan]")
    step1 = connectivity_agent.invoke({
        "input": "Check connectivity issues in C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\starlink_logs.json"
    })
    print(Panel(step1['output'], title="Connectivity Report", border_style="cyan"))

    # ====== Step 2: Personalization ======
    print("[bold green]\n🎬 STEP 2: Personalizing Passenger Experience...[/bold green]")
    step2 = personalization_agent.invoke({
        "input": f"Suggest entertainment and services using C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\passenger_profiles.json\nConnectivity:\n{step1['output']}"
    })
    print(Panel(step2['output'], title="Personalization Suggestions", border_style="green"))

    # ====== Step 3: Suite Layout Suggestion ======
    print("[bold magenta]\n🛋️ STEP 3: Optimizing Qsuite Layout...[/bold magenta]")
    step3 = layout_agent.invoke({
        "input": f"Suggest best Qsuite layout using C:\\Users\\Syed Ayaan\\Projects\\StarlinkOptimizer\\data\\passenger_manifest.json\nPersonalization:\n{step2['output']}"
    })
    print(Panel(step3['output'], title="Qsuite Layout", border_style="magenta"))

    # ====== Step 4: Cabin Crew Briefing ======
    print("[bold yellow]\n🛎️ STEP 4: Generating Final Crew Briefing...[/bold yellow]")
    step4 = crew_alert_agent.invoke({
        "input": f"Create final briefing.\nConnectivity: {step1['output']}\nPersonalization: {step2['output']}\nLayout: {step3['output']}"
    })
    print(Panel(step4['output'], title="Final Cabin Crew Briefing", border_style="yellow"))

if __name__ == "__main__":
    main()
