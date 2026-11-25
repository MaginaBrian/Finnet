import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { LoadingState } from "./StateViews";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, booting } = useAuth();
  const location = useLocation();
  if (booting) return <LoadingState label="Checking your session…" />;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  return children;
}
