export default function UploadCard() {
  return (
    <div className="card" style={{ maxWidth: 720, margin: 'auto' }}>
      <h3>Upload geospatial dataset</h3>

      <div className="dropzone">
        Drag & drop GeoTIFF, Shapefile, GeoJSON, GPKG
      </div>

      <div style={{ marginTop: 12, color: 'var(--text-muted)' }}>
        Detected CRS: EPSG:4326
      </div>

      <select className="select">
        <option>Select target EPSG</option>
      </select>

      <button className="btn-primary" style={{ width: '100%', marginTop: 16 }}>
        Convert CRS
      </button>
    </div>
  );
}
