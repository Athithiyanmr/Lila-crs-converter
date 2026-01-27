import Hero from '../components/Hero';
import UploadCard from '../components/UploadCard';
import Features from '../components/Features';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <>
      <Hero />
      <div style={{ padding: '40px 20px' }}>
        <UploadCard />
      </div>
      <Features />
      <Footer />
    </>
  );
}
