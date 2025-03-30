export default function TestLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return (
      <div style={{
        minHeight: '100vh',
        padding: '20px',
        backgroundColor: '#f0f0f0',
      }}>
        {children}
      </div>
    );
  }