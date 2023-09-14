import { format as dateFnsFormatter } from 'date-fns';

function date(date: string, format = 'longDate') {
  if (!date) return '';

  if (format === 'shortDate') {
    return dateFnsFormatter(new Date(date), 'MMMM d, yyyy');
  }

  if (format === 'longDate') {
    return dateFnsFormatter(new Date(date), 'EEEE, MMMM d, yyyy');
  }

  return dateFnsFormatter(new Date(date), format);
}

export default date;
