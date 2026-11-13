# From Escalation to Intelligent Swarming — the Fireline model

> *Also called: Swarming, Fireline.* A reorganization of the technical
> incident **intake** process for {{company}} — who a request goes to when
> anyone in the company needs help from Technology, Engineering, Data or
> Product.

**Rollout:** {{rollout}} · **Teams in rotation:** {{teams}} · **Paging:** {{stack.paging}}

## The problem with tiered escalation

Before:

```
CS/Support → QA or SRE or CR or PR → Sprint Teams ({{teams}})
```

Support teams must decide, per ticket, which team can help. That creates:

1. **Wrong routing** — nobody knows the correct team for every incident
2. **Process leakage** — help is asked in Slack, mail or phone; the ticket
   loses track and ownership
3. **Sprint interruption** — product teams are "protected" in theory, but get
   contacted directly and spend real time on incidents
4. **Information silos** — communication between Engineering (QA, SRE) and
   Technology teams is unorganized
5. **Information keepers** — only a few people can solve each product's issues,
   because knowledge never spreads
6. **Ticket ping-pong** — issues jump between teams with no real owner

Result: massive delays, at a business *and* human level — and support that
cannot scale.

## The proposal: one front door

After:

```
CS/Support/Sales → Fireline → CR or PR or Sprint Teams ({{teams}})
```

Anyone needing technical help talks to **Fireline**. Fireline either handles
it or escalates it to the right team — with full context.

## What Fireline is

1. A **single point of entry** for all technical incidents
2. A **temporary team, recreated every week**
3. Composed of **one person from each team** ({{teams}})
4. Each team designates one person per week
5. As a team, they gather whatever information an incident needs
6. Because members come from every product, they recognize the nature of any
   technical request quickly
7. Mission: not only urgent matters — **everything solvable fast**
8. Every Fireliner stays ready for any product issue, with extra attention to
   their own team's products
9. Fireliners fix the *lost-in-translation* problem when handing context
   between countries/teams
10. Too big or too complex? They **escape it to a sprint team**, prioritized
    by Product Owners
11. Mission: **protect sprint teams from interruptions**
12. With no incidents open, Fireliners work on their own sprint

## Benefits

- Sprints focus on roadmap, not incident handling
- Large reduction in incident resolution time
- Fewer information keepers — rotation spreads knowledge
- Developers meet production; engineers meet how the product is built
- Fewer silos, no ticket jumping, no "who should I ask?"
- Simpler Support process, simpler tracker projects
- Skill development and a shared sense of team
- **The simpler, the better**

## Fireline rules

### Concepts

| Term | Meaning |
|---|---|
| **Fireline Team** | One engineer from each Technology/Engineering team, assembled every Monday for the week |
| **Fireliner** | A member of that week's team |
| **Fireline Team Leader** | The Fireliner responsible for Fireline working correctly |
| **Monday Meeting** | Weekly handover that creates the new Fireline |
| **Requestor** | Whoever at {{company}} reports the ticket |
| **Ticket qualification** | Identify products involved, correct issue type, severity and urgency |

### Member rules — process

- Qualify every ticket as soon as possible
- Solve everything solvable the same day
- Give the Requestor enough context to answer the customer correctly
- Fireline handles ongoing problems reported by CS and Support
- Team-to-team task requests **do not** go through Fireline — create them
  directly in the other team's backlog
- Update the ticket on every meaningful change (the ticket is the source of
  truth, not Slack)
- Customer Requests → `CR` project for prioritization (CR owns it after)
- Product Requests → `PR` project for prioritization (PO owns it after)
- Not solvable by Fireline → move to the owning team's backlog; PO + team own
  it from that moment

### Member rules — communication

- `#fireline` channel for incoming-ticket talk
- Need help with an incident → ask the Fireline Team Leader
- "Who's on call now?" lives in {{stack.paging}}
- To ping someone, ask the Fireliners first

### Monday meeting

- Weekly rotation meeting, every Monday morning, led by the Team Leader in
  `#fireline` (or a call if needed)
- Outgoing team **hands over context** on every ongoing ticket
- Previous week's tickets released in the tracker

### Reporter rules

- CS first checks whether another CS already knows the answer (`#cs-global`)
- Everything in the ticket is in **English**
- Information must be clear and complete — missing elements? gather them
  before creating a ticket that will interrupt a team
- Bugs: full reproduction steps; screenshots/video if possible
- Keep the conversation **in the ticket**: Slack is fine to move fast, but
  relevant information lands in the ticket afterwards
- You need Fireliners reactive because you have urgencies; they need *you*
  reactive because they have urgencies
- Process questions → `#fireline-support`
- **Blocker urgency wakes Fireliners at 3:00 AM their time — think twice.**

## FAQ

**Will Product be involved?**
No — but they stay close: Fireline creates Product Request tickets with maximum information.

**Doesn't one person per team kill sprint predictability?**
It assumes that predictability is already broken: key engineers are already
interrupted. Swarming spreads ownership until interruptions stop landing on
the same few people.

**Many people aren't ready for Fireline.**
That's the point. Less-experienced members start helping, get mentorship, and
grow. Swarming is the framework that allows that growth.

**What about a huge team working on incidents they don't care about?**
Most cases are solved by the original owner; when help is needed, one
collaborator usually suffices. The "everyone jumps in" fear never happens in
the real world.

**How do we implement it?**
A tracker project with a Kanban board. The details matter less than
communication inside Fireline. Engineering adapts the tracker, Slack,
{{stack.paging}}, calendars and the knowledge base. **Fireliners get
read-only access to production data.**

**Which teams / when?**
Teams: {{teams}} · Rollout: {{rollout}}

## How this fits the rest of the kit

- Severity and roles → `30-incidents/severity-matrix.md`
- What Fireline hands over for big incidents → `30-incidents/postmortem-template.md`
- Read-only production access for Fireliners → `40-agents/guardrails.md`
  (`ai_policy: {{ai_policy}}` applies to agents the same way)

## References

- [Intelligent Swarming (Service Innovation Group)](http://www.serviceinnovation.org/intelligent-swarming/)
- [Swarming: an update (Dr. Ken Wong)](http://www.dbkay.com/intelligent-swarming/intelligent-swarming-an-update)
- [ITSM, DevOps and why the three-tier structure must be replaced with swarming (Jon Hall)](https://medium.com/@JonHall_/itsm-devops-and-why-the-three-tier-structure-must-be-replaced-with-swarming-91e76ba22304)
- [Connected Republic — Digital Swarming (PDF)](http://s3.amazonaws.com/connected_republic/attachments/4/Digital_Swarming_EB_0812c_FINAL.pdf)
