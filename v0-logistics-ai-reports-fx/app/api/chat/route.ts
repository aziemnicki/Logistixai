export const maxDuration = 30

export async function POST(req: Request) {
  try {
    const { message, context } = await req.json()

    // Simulate AI processing delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Generate contextual mock response based on the question
    let response = ""

    const lowerMessage = message.toLowerCase()

    if (
      lowerMessage.includes("deadline") ||
      lowerMessage.includes("compliance") ||
      lowerMessage.includes("requirement")
    ) {
      response = `Based on the "${context.title}" report element, here are the key compliance requirements and deadlines:

**Key Deadlines:**
- Initial assessment and gap analysis: Q2 2024
- Implementation of technical measures: Q4 2024
- Full compliance required: January 2025

**Compliance Requirements:**
- Risk management procedures must be documented and regularly updated
- Incident reporting mechanisms must be established within 24 hours of detection
- Regular security audits and penetration testing (minimum quarterly)
- Staff training programs on cybersecurity awareness

These requirements align with NIS2 Directive Article 21 and should be prioritized in your implementation roadmap.`
    } else if (
      lowerMessage.includes("impact") ||
      lowerMessage.includes("operation") ||
      lowerMessage.includes("action") ||
      lowerMessage.includes("prioritize")
    ) {
      response = `The "${context.title}" has significant operational implications:

**Immediate Impact:**
- Current security protocols may need enhancement to meet new standards
- Additional documentation and reporting processes required
- Potential need for new security infrastructure investments

**Priority Actions:**
1. Conduct comprehensive gap analysis against new requirements (2-3 weeks)
2. Establish incident response team and procedures (1 month)
3. Implement enhanced monitoring and logging systems (2-3 months)
4. Develop staff training program (ongoing)

**Resource Requirements:**
- Estimated budget: €50,000-150,000 depending on current security maturity
- Dedicated compliance officer or team recommended
- External consultancy for initial assessment: €15,000-25,000

I recommend starting with the gap analysis to identify specific areas requiring immediate attention.`
    } else if (
      lowerMessage.includes("implementation") ||
      lowerMessage.includes("cost") ||
      lowerMessage.includes("step") ||
      lowerMessage.includes("detail")
    ) {
      response = `Here's a detailed implementation roadmap for "${context.title}":

**Phase 1: Assessment (Weeks 1-4)**
- Conduct security audit and gap analysis
- Document current processes and systems
- Identify compliance gaps
- Cost: €15,000-25,000

**Phase 2: Planning (Weeks 5-8)**
- Develop implementation strategy
- Define roles and responsibilities
- Create project timeline and budget
- Cost: Internal resources + €10,000 consulting

**Phase 3: Implementation (Months 3-6)**
- Deploy technical security measures
- Establish incident response procedures
- Implement monitoring and logging systems
- Staff training programs
- Cost: €50,000-100,000

**Phase 4: Validation (Months 7-8)**
- Internal audits and testing
- Documentation review
- Compliance verification
- Cost: €10,000-20,000

**Total Estimated Investment:** €85,000-155,000 over 8 months. This includes technology, consulting, and internal resource allocation.`
    } else {
      response = `Thank you for your question about "${context.title}". 

This report element highlights important regulatory and operational considerations for your logistics operations. The key points to consider are:

**Main Considerations:**
- Regulatory compliance requirements are evolving rapidly in the European transport sector
- Proactive implementation of security and compliance measures reduces long-term costs
- Documentation and process formalization are critical for demonstrating compliance

**Recommended Next Steps:**
1. Review the full report element details carefully
2. Assess your current state against the requirements outlined
3. Engage relevant stakeholders (IT, operations, legal) in planning
4. Consider external expertise for complex regulatory interpretations

Would you like me to provide more specific information about any particular aspect of this report element? Feel free to ask about deadlines, costs, implementation steps, or operational impacts.`
    }

    return new Response(JSON.stringify({ response }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    })
  } catch (error) {
    console.error("[v0] Chat API error:", error)
    return new Response(
      JSON.stringify({
        error: "Failed to generate response",
        message: error instanceof Error ? error.message : "Unknown error",
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
        },
      },
    )
  }
}
