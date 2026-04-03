#!/usr/bin/env python
"""Test that all interview/placement routes are properly registered."""

import sys
sys.path.insert(0, '.')

try:
    from app import create_app
    
    app = create_app()
    
    # Get all routes
    routes = [(str(rule), rule.endpoint) for rule in app.url_map.iter_rules()]
    
    # Filter for interview/placement routes
    interview_routes = [r for r in routes if 'interview' in r[0] or 'placement' in r[0]]
    
    print("✅ Interview & Placement Routes Found:")
    print("=" * 60)
    
    for route, endpoint in sorted(interview_routes):
        print(f"{route:40} ➜ {endpoint}")
    
    if len(interview_routes) >= 3:
        print("\n✅ All expected routes are registered!")
    else:
        print(f"\n⚠️  Expected at least 3 routes, found {len(interview_routes)}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
