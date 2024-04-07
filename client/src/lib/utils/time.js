// time calculations
export function calculateRecency(dateString) {
    const today = new Date();
    const incidentDate = new Date(dateString.replace(/-/g, '/')); // Ensure compatibility
  
    const differenceInTime = today.getTime() - incidentDate.getTime();
    const differenceInDays = differenceInTime / (1000 * 3600 * 24);
  
    return Math.floor(differenceInDays);
  }
  
  