import { motion, useAnimation } from 'framer-motion';
import { useEffect } from 'react';

interface FloatCardProps {
  children: React.ReactNode;
  delay?: number;
  floatDuration?: number;
  floatOffset?: number;
  style?: React.CSSProperties;
  zIndex?: number;
}

function FloatCard({
  children,
  delay = 0,
  floatDuration = 6,
  floatOffset = 10,
  style,
  zIndex = 1,
}: FloatCardProps) {
  const controls = useAnimation();

  useEffect(() => {
    controls
      .start({
        opacity: 1,
        y: 0,
        scale: 1,
        transition: { type: 'spring', stiffness: 180, damping: 22, delay },
      })
      .then(() => {
        controls.start({
          y: [0, -floatOffset, 0],
          transition: { duration: floatDuration, repeat: Infinity, ease: 'easeInOut' },
        });
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <motion.div
      initial={{ opacity: 0, y: 28, scale: 0.93 }}
      animate={controls}
      className="glass-card"
      style={{ position: 'absolute', zIndex, ...style }}
    >
      {children}
    </motion.div>
  );
}

// ── Card 1: Platform Status ──────────────────────────────────────────────────
function PlatformStatusCard() {
  const services = [
    { name: 'InsureDesk Portal', status: 'All systems nominal' },
    { name: 'AI Engine',         status: 'Processing 14 cases' },
    { name: 'FAST Admin',        status: 'Policy sync active'  },
  ];
  return (
    <div style={{ width: 218, padding: '16px 18px' }}>
      <p style={labelCaps}>Platform Status</p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {services.map(({ name, status }) => (
          <div key={name} style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
            <span style={{
              marginTop: 4, flexShrink: 0,
              width: 6, height: 6, borderRadius: '50%',
              background: '#22c55e',
              boxShadow: '0 0 6px rgba(34,197,94,0.7)',
              display: 'block',
              animation: 'livePulse 2s ease-in-out infinite',
            }} />
            <div>
              <p style={{ fontSize: '0.72rem', fontWeight: 600, color: '#d9e2ec', lineHeight: 1.3, marginBottom: 1 }}>
                {name}
              </p>
              <p style={{ fontSize: '0.6rem', color: '#627d98', fontFamily: 'ui-monospace, monospace' }}>
                {status}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Card 2: AI Engine Risk Score ─────────────────────────────────────────────
function AIEngineCard() {
  return (
    <div style={{ width: 205, padding: '16px 18px' }}>
      <p style={labelCaps}>AI Underwriting</p>
      <p style={{ fontSize: '0.6rem', color: '#486581', fontFamily: 'ui-monospace, monospace', marginBottom: 12 }}>
        Case #4821
      </p>
      <div style={{ marginBottom: 12 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
          <span style={{ fontSize: '0.52rem', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase' as const, color: '#627d98' }}>
            Risk Score
          </span>
          <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#d9e2ec', letterSpacing: '-0.02em' }}>82</span>
        </div>
        <div style={{ height: 4, borderRadius: 2, background: 'rgba(59,130,246,0.10)', overflow: 'hidden' }}>
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: '82%' }}
            transition={{ duration: 1.4, ease: 'easeOut', delay: 1.0 }}
            style={{ height: '100%', borderRadius: 2, background: 'linear-gradient(90deg, #2563eb 0%, #60a5fa 100%)' }}
          />
        </div>
      </div>
      <div style={{
        display: 'flex', alignItems: 'center', gap: 6,
        padding: '6px 10px', borderRadius: 6,
        background: 'rgba(34,197,94,0.10)',
        border: '1px solid rgba(34,197,94,0.30)',
      }}>
        <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#22c55e', flexShrink: 0, display: 'block' }} />
        <span style={{ fontSize: '0.58rem', fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase' as const, color: '#86efac' }}>
          Auto-Approve
        </span>
      </div>
    </div>
  );
}

// ── Card 3: Active Workflow ──────────────────────────────────────────────────
function WorkflowCard() {
  const steps = [
    { label: 'Intake',     done: true  },
    { label: 'AI Review',  done: true  },
    { label: 'Bind',       done: false },
  ];
  return (
    <div style={{ width: 276, padding: '16px 18px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
        <p style={labelCaps}>Active Workflow</p>
        <span style={{ fontSize: '0.58rem', color: '#334e68', fontFamily: 'ui-monospace, monospace' }}>#4821</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 0, marginBottom: 12 }}>
        {steps.map((step, i) => (
          <div key={step.label} style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
              <div style={{
                width: 24, height: 24, borderRadius: '50%',
                background: step.done ? 'rgba(59,130,246,0.18)' : 'rgba(59,130,246,0.05)',
                border: `1.5px solid ${step.done ? 'rgba(96,165,250,0.65)' : 'rgba(59,130,246,0.18)'}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                {step.done ? (
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5l2.5 2.5L8 3" stroke="#60a5fa" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                ) : (
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'rgba(59,130,246,0.25)', display: 'block' }} />
                )}
              </div>
              <span style={{ fontSize: '0.55rem', color: step.done ? '#829ab1' : '#334e68', fontFamily: 'ui-monospace, monospace', whiteSpace: 'nowrap' as const }}>
                {step.label}
              </span>
            </div>
            {i < steps.length - 1 && (
              <div style={{ width: 28, height: 1.5, background: i === 0 ? 'rgba(59,130,246,0.5)' : 'rgba(59,130,246,0.14)', marginBottom: 16, flexShrink: 0 }} />
            )}
          </div>
        ))}
      </div>
      <div style={{ height: 3, borderRadius: 2, background: 'rgba(59,130,246,0.08)', overflow: 'hidden', marginBottom: 8 }}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: '56%' }}
          transition={{ duration: 1.5, ease: 'easeOut', delay: 1.3 }}
          style={{ height: '100%', borderRadius: 2, background: 'linear-gradient(90deg, #2563eb, #60a5fa)' }}
        />
      </div>
      <p style={{ fontSize: '0.6rem', color: '#334e68', fontFamily: 'ui-monospace, monospace' }}>
        Step 2 of 3 · 31h remaining
      </p>
    </div>
  );
}

// ── Card 4: Impact Metric ────────────────────────────────────────────────────
function MetricCard() {
  return (
    <div style={{ width: 128, padding: '14px 16px' }}>
      <p style={{ ...labelCaps, marginBottom: 8 }}>Engagement</p>
      <p style={{ fontSize: '1.9rem', fontWeight: 800, color: '#d9e2ec', letterSpacing: '-0.03em', lineHeight: 1, marginBottom: 4 }}>
        +34%
      </p>
      <p style={{ fontSize: '0.65rem', fontWeight: 500, color: '#627d98' }}>WAU Lift</p>
      <p style={{ fontSize: '0.55rem', color: '#334e68', fontFamily: 'ui-monospace, monospace', marginTop: 3 }}>60-day rollout</p>
    </div>
  );
}

// ── Card 5: Live Event ───────────────────────────────────────────────────────
function LiveEventCard() {
  return (
    <div style={{ width: 190, padding: '14px 16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
        <span style={{
          width: 6, height: 6, borderRadius: '50%',
          background: '#22c55e',
          boxShadow: '0 0 6px rgba(34,197,94,0.8)',
          display: 'block',
          animation: 'livePulse 1.8s ease-in-out infinite',
        }} />
        <span style={{ fontSize: '0.5rem', fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase' as const, color: '#22c55e' }}>
          Live
        </span>
      </div>
      <p style={{ fontSize: '0.78rem', fontWeight: 600, color: '#d9e2ec', marginBottom: 3, lineHeight: 1.3 }}>
        Policy #4819 bound
      </p>
      <p style={{ fontSize: '0.62rem', color: '#627d98' }}>Annuity · Fixed</p>
      <p style={{ fontSize: '0.55rem', color: '#334e68', fontFamily: 'ui-monospace, monospace', marginTop: 6 }}>2s ago</p>
    </div>
  );
}

// ── Shared style ─────────────────────────────────────────────────────────────
const labelCaps: React.CSSProperties = {
  fontSize: '0.5rem',
  fontWeight: 700,
  letterSpacing: '0.18em',
  textTransform: 'uppercase',
  color: '#60a5fa',
  marginBottom: 12,
};

// ── Main composition ─────────────────────────────────────────────────────────
export default function HeroComposition() {
  return (
    <div style={{ position: 'relative', width: '100%', height: 540 }} aria-hidden="true">
      {/* Ambient glow behind cards */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse 80% 60% at 50% 45%, rgba(59,130,246,0.07) 0%, transparent 70%)',
      }} />

      <FloatCard delay={0.25} floatDuration={5.5} floatOffset={10} zIndex={3} style={{ top: 0, left: 0 }}>
        <PlatformStatusCard />
      </FloatCard>

      <FloatCard delay={0.5} floatDuration={7.2} floatOffset={14} zIndex={2} style={{ top: 44, right: 0 }}>
        <AIEngineCard />
      </FloatCard>

      <FloatCard delay={0.85} floatDuration={6} floatOffset={8} zIndex={4} style={{ top: 208, left: 36 }}>
        <WorkflowCard />
      </FloatCard>

      <FloatCard delay={0.38} floatDuration={4.8} floatOffset={12} zIndex={2} style={{ bottom: 88, left: 4 }}>
        <MetricCard />
      </FloatCard>

      <FloatCard delay={0.65} floatDuration={6.5} floatOffset={10} zIndex={3} style={{ bottom: 28, right: 0 }}>
        <LiveEventCard />
      </FloatCard>
    </div>
  );
}
