import { useEffect } from "react";

export function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} | FinTrack` : "FinTrack by Finnet Technologies";
  }, [title]);
}
