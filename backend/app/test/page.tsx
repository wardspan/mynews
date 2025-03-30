'use client';

export default function TestPage() {
  // Log to see if this component is rendering
  console.log('TestPage is rendering');
  
  return (
    <div style={{
      padding: '40px',
      backgroundColor: 'yellow',
      color: 'black',
      fontFamily: 'Arial',
      fontSize: '24px',
      border: '5px solid red',
      borderRadius: '10px',
      margin: '100px',
      textAlign: 'center',
    }}>
      <h1>TEST PAGE</h1>
      <p>If you can see this, your Next.js app is working!</p>
      <button 
        style={{
          padding: '10px 20px',
          backgroundColor: 'blue',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px',
        }}
        onClick={() => {
          alert('Button clicked!');
          console.log('Button clicked in browser console');
        }}
      >
        Click Me
      </button>
    </div>
  );
}