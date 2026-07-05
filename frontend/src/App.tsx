import { RealityProvider } from './context/RealityContext';
import DashboardLayout from './components/DashboardLayout';

function App() {
  return (
    <RealityProvider>
      <DashboardLayout />
    </RealityProvider>
  );
}

export default App;
