"use client";

const COUNTRY_FLAGS: Record<string, string> = {
  de: "🇩🇪",
  fr: "🇫🇷",
  nl: "🇳🇱",
  at: "🇦🇹",
  ch: "🇨🇭",
};

export type Job = {
  title: string;
  company: string;
  location: string;
  country: string;
  salary: string;
  score: number;
  url: string;
  posted: string;
  remote: boolean;
};

function ScoreBadge({ score }: { score: number }) {
  const color = score >= 8 ? "#22c55e" : score >= 6 ? "#eab308" : "#6b7280";
  return (
    <span
      style={{
        background: color + "22",
        color,
        border: `1px solid ${color}44`,
        borderRadius: 6,
        padding: "2px 10px",
        fontSize: 13,
        fontWeight: 700,
      }}
    >
      {score}/10
    </span>
  );
}

function Chip({
  children,
  accent,
  muted,
}: {
  children: React.ReactNode;
  accent?: boolean;
  muted?: boolean;
}) {
  return (
    <span
      style={{
        fontSize: 12,
        padding: "3px 10px",
        borderRadius: 20,
        background: accent ? "#3b82f622" : muted ? "#ffffff08" : "#ffffff10",
        color: accent ? "#60a5fa" : muted ? "#666" : "#ccc",
        border: accent ? "1px solid #3b82f633" : "1px solid #ffffff10",
      }}
    >
      {children}
    </span>
  );
}

function JobCard({ job }: { job: Job }) {
  return (
    <a
      href={job.url}
      target="_blank"
      rel="noopener noreferrer"
      style={{ textDecoration: "none", color: "inherit" }}
    >
      <div
        style={{
          background: "#1a1a1a",
          border: "1px solid #2a2a2a",
          borderRadius: 12,
          padding: "20px 24px",
          cursor: "pointer",
          transition: "border-color 0.15s",
        }}
        onMouseEnter={(e) =>
          ((e.currentTarget as HTMLDivElement).style.borderColor = "#444")
        }
        onMouseLeave={(e) =>
          ((e.currentTarget as HTMLDivElement).style.borderColor = "#2a2a2a")
        }
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: 12,
          }}
        >
          <div style={{ flex: 1 }}>
            <div
              style={{
                fontSize: 17,
                fontWeight: 600,
                marginBottom: 4,
                lineHeight: 1.3,
              }}
            >
              {job.title}
            </div>
            <div style={{ fontSize: 14, color: "#a0a0a0", marginBottom: 12 }}>
              {job.company}
            </div>
          </div>
          <ScoreBadge score={job.score} />
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          <Chip>
            {COUNTRY_FLAGS[job.country] ?? "🌍"} {job.location}
          </Chip>
          {job.remote && <Chip accent>Remote / Hybrid</Chip>}
          {job.salary !== "Not listed" && <Chip>{job.salary}</Chip>}
          <Chip muted>{job.posted}</Chip>
        </div>
      </div>
    </a>
  );
}

function Section({
  title,
  subtitle,
  jobs,
}: {
  title: string;
  subtitle: string;
  jobs: Job[];
}) {
  if (jobs.length === 0) return null;
  return (
    <section style={{ marginBottom: 48 }}>
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 10,
          marginBottom: 16,
        }}
      >
        <h2 style={{ fontSize: 18, fontWeight: 600, margin: 0 }}>{title}</h2>
        <span style={{ color: "#555", fontSize: 13 }}>
          {subtitle} · {jobs.length} roles
        </span>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {jobs.map((job, i) => (
          <JobCard key={i} job={job} />
        ))}
      </div>
    </section>
  );
}

export function JobList({ jobs }: { jobs: Job[] }) {
  const top = jobs.filter((j) => j.score >= 8);
  const good = jobs.filter((j) => j.score >= 6 && j.score < 8);
  const rest = jobs.filter((j) => j.score < 6);

  return (
    <>
      <Section title="🟢 Top Picks" subtitle="Score 8–10" jobs={top} />
      <Section title="🟡 Good Matches" subtitle="Score 6–7" jobs={good} />
      <Section title="⚪ Other Roles" subtitle="Score below 6" jobs={rest} />
    </>
  );
}
