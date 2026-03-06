import { motion } from 'framer-motion';
import { Camera, Zap, Heart, ArrowRight, ChefHat } from 'lucide-react';

export default function LandingPage({ onStart }) {
    return (
        <div className="landing-page">
            <header className="container" style={{ padding: '2rem 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <ChefHat size={32} className="gradient-text" style={{ color: '#f59e0b' }} />
                    <h2 style={{ fontSize: '1.5rem' }}>Kitchen <span className="gradient-text">Vision</span></h2>
                </div>
            </header>

            <main className="container animate-fade-in" style={{ marginTop: '4rem', textAlign: 'center' }}>
                <motion.h1
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6 }}
                    style={{ fontSize: '4.5rem', lineHeight: '1.1', marginBottom: '1.5rem' }}
                >
                    Transform Your Pantry into <br />
                    <span className="gradient-text">Gourmet Masterpieces</span>
                </motion.h1>

                <p style={{ fontSize: '1.25rem', color: 'var(--text-muted)', maxWidth: '700px', margin: '0 auto 3rem' }}>
                    Stop staring at your fridge. Our AI vision instantly analyzes your ingredients and generates healthy, personalized recipes in seconds.
                </p>

                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={onStart}
                    style={{
                        background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                        color: 'white',
                        padding: '1.25rem 3rem',
                        borderRadius: '9999px',
                        fontSize: '1.1rem',
                        fontWeight: '600',
                        border: 'none',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.75rem',
                        boxShadow: '0 20px 25px -5px rgba(245, 158, 11, 0.3)'
                    }}
                >
                    Launch Assistant <ArrowRight size={20} />
                </motion.button>

                <div className="features-grid" style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '2rem',
                    marginTop: '8rem',
                    marginBottom: '4rem'
                }}>
                    <FeatureCard
                        icon={<Camera className="gradient-text" />}
                        title="AI Vision Analysis"
                        desc="Snapshot your pantry. We identify every item with 98% accuracy."
                    />
                    <FeatureCard
                        icon={<Zap className="gradient-text" />}
                        title="Instant Recipes"
                        desc="3-step beginner-friendly recipes tailored to your current inventory."
                    />
                    <FeatureCard
                        icon={<Heart className="gradient-text" />}
                        title="Health Tracking"
                        desc="Every recipe includes a nutritional score and healthy tips."
                    />
                </div>
            </main>

            <footer style={{ borderTop: '1px solid var(--glass-border)', padding: '4rem 0', marginTop: '4rem' }}>
                <div className="container" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                    <p>&copy; 2025 Kitchen Vision Pro. Powered by Gemini 2.5.</p>
                </div>
            </footer>
        </div>
    );
}

function FeatureCard({ icon, title, desc }) {
    return (
        <div className="glass" style={{ padding: '2.5rem', textAlign: 'left' }}>
            <div style={{ marginBottom: '1.5rem' }}>{icon}</div>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>{title}</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>{desc}</p>
        </div>
    );
}
