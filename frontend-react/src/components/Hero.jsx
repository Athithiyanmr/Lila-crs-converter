export default function Hero() {
  return (
    <section style={{ padding: '80px 20px', textAlign: 'center' }}>
      <h1 style={{ fontSize: '3rem', fontWeight: 800 }}>🌍 Geo CRS Converter</h1>
      <p style={{ color: 'var(--text-muted)', maxWidth: 720, margin: '16px auto' }}>
        Reproject raster and vector geospatial datasets instantly.
      </p>

      <div style={{ marginTop: 24 }}>
        <button className="btn-primary">Upload dataset</button>
        <a href="https://github.com/Athithiyanmr/geo-crs-converter" target="_blank"
           style={{ marginLeft: 16, color: 'var(--accent)' }}>
           View on GitHub →
        </a>
      </div>
    </section>
  );
}
