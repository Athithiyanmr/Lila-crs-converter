const features = [
  "Raster reprojection (GeoTIFF)",
  "Vector reprojection (Shapefile, GeoJSON, GPKG)",
  "Automatic CRS detection",
  "GDAL-powered backend",
  "Dockerized deployment",
  "Web-based interface"
];

export default function Features() {
  return (
    <section style={{ padding: '60px 20px', maxWidth: 900, margin: 'auto' }}>
      <h2 style={{ textAlign: 'center' }}>Features</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))', gap: 16 }}>
        {features.map(f => (
          <div key={f} className="card" style={{ textAlign: 'center' }}>{f}</div>
        ))}
      </div>
    </section>
  );
}
