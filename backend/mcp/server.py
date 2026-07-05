import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for Gemini connections
mcp = FastMCP(
    "ECHO RealityVerse Server",
    description="Provides tools and resources to interact with user habits and RealityVerse 3D planet states."
)

@mcp.tool()
def retrieve_habits_summary(limit: int = 10) -> str:
    """
    Retrieve a brief summary of recently logged habits.
    Helpful for contextualizing the user's focus, health, and budget trends.
    """
    return f"FastMCP: Retrieved last {limit} user habit logs. Base indicators are balanced."

@mcp.tool()
def project_metric_impact(category: str, score: float) -> str:
    """
    Exposes dry-run calculations to predict how a future habit (e.g. category='focus', score=0.9)
    will impact the target biome governor.
    """
    projected_change = (score - 0.5) * 0.2
    return f"FastMCP: Projected impact of {category} habits with rating {score:.2f} is {projected_change:+.2f} shift in the corresponding governor biome."

@mcp.resource("reality://planet/current_state")
def query_planet_resource() -> str:
    """
    Exposes the latest snapshot of the RealityVerse planet's 3D configurations.
    """
    return '{"forest_health": 0.5, "ocean_health": 0.5, "finance_health": 0.5, "focus_health": 0.5, "overall_equilibrium": 0.5, "agent_version": "v2.0.0-ADK"}'

if __name__ == "__main__":
    mcp.run()
