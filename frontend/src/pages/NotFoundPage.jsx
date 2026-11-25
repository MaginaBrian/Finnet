import { Link } from "react-router-dom";
import { useDocumentTitle } from "../hooks/useDocumentTitle";
import { EmptyState } from "../components/StateViews";

export default function NotFoundPage() {
  useDocumentTitle("Page not found");
  return (
    <div className="panel">
      <EmptyState title="Page not found" action={<Link className="btn btn--primary" to="/">Go to portfolios</Link>}>
        The page you're looking for doesn't exist or has moved.
      </EmptyState>
    </div>
  );
}
