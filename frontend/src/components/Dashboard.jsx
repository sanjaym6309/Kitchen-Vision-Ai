import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, ChevronLeft, Loader2, ListChecks, Utensils, Activity, ShoppingCart } from 'lucide-react';

const API_URL = 'http://127.0.0.1:8000';

export default function Dashboard({ onBack }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null); // { ingredients, categorized }
    const [recipes, setRecipes] = useState(null);
    const [grocery, setGrocery] = useState({}); // recipeTitle -> groceryData
    const [history, setHistory] = useState([]);
    const [showHistory, setShowHistory] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await axios.get(`${API_URL}/api/history`);
            setHistory(res.data.history);
        } catch (err) {
            console.error("Failed to fetch history", err);
        }
    };


    const handleUpload = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;

        setFile(selectedFile);
        setLoading(true);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const res = await axios.post(`${API_URL}/api/analyze`, formData);
            setResults(res.data);
            fetchHistory(); // Refresh history sidebar

            // Auto-trigger recipe generation

            const recipeRes = await axios.post(`${API_URL}/api/recipes`, {
                ingredients: res.data.ingredients
            });
            setRecipes(recipeRes.data.recipes);
        } catch (err) {
            console.error(err);
            alert("Failed to analyze image. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    const fetchGrocery = async (recipe) => {
        if (grocery[recipe.title]) return;

        try {
            const res = await axios.post(`${API_URL}/api/grocery`, {
                available: results.ingredients,
                recipe: recipe.ingredients_needed
            });
            setGrocery(prev => ({ ...prev, [recipe.title]: res.data.grocery }));
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="dashboard container" style={{ padding: '2rem 0' }}>
            <header style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '3rem', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <button
                        onClick={onBack}
                        style={{ background: 'none', border: 'none', color: 'var(--text-muted)' }}
                    >
                        <ChevronLeft size={24} />
                    </button>
                    <h1>Smart Dashboard</h1>
                </div>

                <button
                    onClick={() => setShowHistory(!showHistory)}
                    className="glass"
                    style={{ padding: '0.75rem 1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'white' }}
                >
                    <ListChecks size={20} /> History
                </button>
            </header>

            <AnimatePresence>
                {showHistory && (
                    <motion.div
                        initial={{ x: '100%' }}
                        animate={{ x: 0 }}
                        exit={{ x: '100%' }}
                        style={{
                            position: 'fixed',
                            top: 0,
                            right: 0,
                            width: '400px',
                            height: '100vh',
                            background: 'rgba(15, 23, 42, 0.95)',
                            backdropFilter: 'blur(20px)',
                            borderLeft: '1px solid var(--glass-border)',
                            zIndex: 1000,
                            padding: '2rem',
                            boxShadow: '-20px 0 25px -5px rgba(0,0,0,0.5)',
                            overflowY: 'auto'
                        }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                            <h2 style={{ fontSize: '1.5rem' }}>Recent Scans</h2>
                            <button onClick={() => setShowHistory(false)} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>✕</button>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {history.length === 0 ? <p style={{ color: 'var(--text-muted)' }}>No history yet.</p> : (
                                history.map((h) => (
                                    <motion.div
                                        key={h.id}
                                        whileHover={{ scale: 1.02 }}
                                        className="glass"
                                        onClick={() => {
                                            setResults({ ingredients: h.ingredients, categorized: h.categorized });
                                            setRecipes(h.recipes);
                                            setShowHistory(false);
                                        }}
                                        style={{ padding: '1.25rem', cursor: 'pointer', transition: '0.3s', border: '1px solid var(--glass-border)' }}
                                    >
                                        <div style={{ fontSize: '0.75rem', color: '#f59e0b', fontWeight: 'bold', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                                            {new Date(h.timestamp).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                        <div style={{ fontSize: '0.85rem', color: 'white', opacity: 0.9 }}>
                                            {h.ingredients.slice(0, 3).join(', ')}...
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>


            {!results && (
                <motion.div
                    className="glass"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{ padding: '5rem', textAlign: 'center', borderStyle: 'dashed', borderWidth: '2px' }}
                >
                    <label style={{ cursor: 'pointer' }}>
                        <input type="file" hidden onChange={handleUpload} accept="image/*" />
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem' }}>
                            <div style={{ background: 'rgba(245,158,11,0.1)', padding: '2rem', borderRadius: '50%' }}>
                                {loading ? <Loader2 className="animate-spin" size={48} color="#f59e0b" /> : <Upload size={48} color="#f59e0b" />}
                            </div>
                            <div>
                                <h3 style={{ fontSize: '1.5rem' }}>{loading ? 'Analyzing your pantry...' : 'Upload Pantry Image'}</h3>
                                <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                    Drag and drop or click to browse (PNG, JPG)
                                </p>
                            </div>
                        </div>
                    </label>
                </motion.div>
            )}

            {results && (
                <div className="results-layout" style={{ display: 'grid', gap: '3rem' }}>
                    <section className="pantry-section">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                            <ListChecks className="gradient-text" />
                            <h2>Categorized Pantry</h2>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem' }}>
                            {Object.entries(results.categorized).map(([cat, items]) => (
                                <div key={cat} className="glass" style={{ padding: '1.5rem' }}>
                                    <h4 style={{ color: 'var(--primary)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        {cat} <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>({items.length})</span>
                                    </h4>
                                    <ul style={{ listStyle: 'none', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                                        {items.slice(0, 10).map(item => <li key={item} style={{ marginBottom: '0.3rem' }}>• {item}</li>)}
                                        {items.length > 10 && <li>+ {items.length - 10} more</li>}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </section>

                    {recipes && (
                        <section className="recipes-section">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                                <Utensils className="gradient-text" />
                                <h2>Recommended Recipes</h2>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
                                {recipes.map((recipe, idx) => (
                                    <RecipeCard
                                        key={idx}
                                        recipe={recipe}
                                        grocery={grocery[recipe.title]}
                                        onReveal={() => fetchGrocery(recipe)}
                                    />
                                ))}
                            </div>
                        </section>
                    )}
                </div>
            )}
        </div>
    );
}

function RecipeCard({ recipe, grocery, onReveal }) {
    const [showGrocery, setShowGrocery] = useState(false);

    return (
        <motion.div
            className="glass"
            whileHover={{ y: -10 }}
            style={{ padding: '2rem', display: 'flex', flexDirection: 'column' }}
        >
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                <span style={{ background: 'rgba(245,158,11,0.1)', padding: '0.25rem 0.75rem', borderRadius: 'full', color: '#f59e0b', fontSize: '0.8rem' }}>
                    {recipe.prep_time_mins} mins
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--success)' }}>
                    <Activity size={16} /> <span>{recipe.health_score}/10</span>
                </div>
            </div>

            <h3 style={{ marginBottom: '1rem' }}>{recipe.title}</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>{recipe.health_explanation}</p>

            <div style={{ marginBottom: '1.5rem' }}>
                <h5 style={{ marginBottom: '0.5rem', fontSize: '0.9rem' }}>Instructions (3 Steps)</h5>
                <ol style={{ paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'white' }}>
                    {recipe.instructions_3_steps.map((s, i) => <li key={i} style={{ marginBottom: '0.5rem' }}>{s}</li>)}
                </ol>
            </div>

            <button
                onClick={() => { setShowGrocery(!showGrocery); onReveal(); }}
                style={{
                    marginTop: 'auto',
                    background: 'var(--glass-border)',
                    border: '1px solid var(--glass-border)',
                    color: 'white',
                    padding: '0.75rem',
                    borderRadius: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '0.5rem'
                }}
            >
                <ShoppingCart size={18} /> {showGrocery ? 'Hide Grocery' : 'View Grocery List'}
            </button>

            <AnimatePresence>
                {showGrocery && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        style={{ overflow: 'hidden', marginTop: '1rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}
                    >
                        <h5 style={{ marginBottom: '0.5rem', fontSize: '0.85rem' }}>Missing & Substitutions</h5>
                        {!grocery ? <div style={{ display: 'flex', justifyContent: 'center' }}><Loader2 className="animate-spin" size={20} /></div> : (
                            grocery.length === 0 ? <p style={{ fontSize: '0.8rem', color: 'var(--success)' }}>You have everything!</p> : (
                                <ul style={{ listStyle: 'none' }}>
                                    {grocery.map((g, i) => (
                                        <li key={i} style={{ fontSize: '0.8rem', marginBottom: '0.5rem' }}>
                                            <span style={{ color: 'var(--danger)' }}>• {g.missing_item}</span>
                                            <br />
                                            <span style={{ opacity: 0.6 }}>Sub: {g.substitutes.join(', ')}</span>
                                        </li>
                                    ))}
                                </ul>
                            )
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
