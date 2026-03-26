import sqlglot
from sqlglot import exp
from typing import List, Set, Tuple, Dict, Optional
import re

class LineageParser:
    @staticmethod
    def extract_tables(sql: str) -> Tuple[Set[str], Set[str], List[Dict[str, Any]]]:
        """
        Extracts source and destination tables, and relationships (with columns).
        Returns (sources, destinations, relationships)
        """
        sources = set()
        destinations = set()
        relationships = []
        
        if not sql:
            return sources, destinations, relationships

        try:
            expressions = sqlglot.parse(sql, read="bigquery")
            
            for expression in expressions:
                # 1. Find Destinations
                current_destinations = set()
                for ddl_dml in [exp.Create, exp.Insert, exp.Merge, exp.Update]:
                    for found in expression.find_all(ddl_dml):
                        table = found.find(exp.Table)
                        if table:
                            name = LineageParser._format_table(table)
                            destinations.add(name)
                            current_destinations.add(name)

                # 2. Find Sources & Relationships
                # We need to link sources to the destinations in this specific query
                query_sources = set()
                
                # Check Joins for columns
                join_columns = []
                for join in expression.find_all(exp.Join):
                    table = join.find(exp.Table)
                    if table:
                        src_name = LineageParser._format_table(table)
                        query_sources.add(src_name)
                        # Extract columns from 'ON' or 'USING'
                        on = join.args.get("on")
                        if on:
                            cols = [c.sql() for c in on.find_all(exp.Column)]
                            join_columns.extend(cols)

                # From clause
                for from_clause in expression.find_all(exp.From):
                    for table in from_clause.find_all(exp.Table):
                        query_sources.add(LineageParser._format_table(table))

                # Merge sources
                for merge in expression.find_all(exp.Merge):
                    using = merge.args.get("using")
                    if using:
                        for table in using.find_all(exp.Table):
                            query_sources.add(LineageParser._format_table(table))
                    
                    on = merge.args.get("on")
                    if on:
                        join_columns.extend([c.sql() for c in on.find_all(exp.Column)])

                sources.update(query_sources)
                
                # Create relationship objects
                rel_label = ", ".join(list(set(join_columns))[:3]) # Limit labels to first 3 columns
                if not rel_label:
                    rel_label = "SELECT/INSERT"

                for d in current_destinations:
                    for s in query_sources:
                        if s != d:
                            relationships.append({
                                "source": s,
                                "target": d,
                                "columns": rel_label
                            })

        except Exception as e:
            print(f"Error parsing SQL: {e}")
            # Minimal fallback
            src_regex = re.findall(r'(?:FROM|JOIN)\s+`?([\w\.-]+)`?', sql, re.IGNORECASE)
            dest_regex = re.findall(r'(?:INSERT\s+INTO|CREATE\s+TABLE|MERGE|UPDATE)\s+`?([\w\.-]+)`?', sql, re.IGNORECASE)
            sources.update(src_regex)
            destinations.update(dest_regex)
            for d in dest_regex:
                for s in src_regex:
                    if s != d:
                        relationships.append({"source": s, "target": d, "columns": "regex_fallback"})

        return sources - destinations, destinations, relationships

    @staticmethod
    def _format_table(table: exp.Table) -> str:
        parts = []
        if table.args.get("catalog"):
            parts.append(str(table.args["catalog"].this))
        if table.args.get("db"):
            parts.append(str(table.args["db"].this))
        if table.args.get("this"):
            parts.append(str(table.args["this"].this))
        
        return ".".join(parts).replace("`", "")
